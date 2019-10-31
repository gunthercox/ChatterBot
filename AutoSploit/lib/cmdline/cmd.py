import os
import sys
import random
import argparse

import lib.output
import lib.jsonize
import lib.settings
import api_calls.censys
import api_calls.shodan
import api_calls.zoomeye
import lib.exploitation.exploiter


class AutoSploitParser(argparse.ArgumentParser):

    def __init__(self):
        super(AutoSploitParser, self).__init__()

    @staticmethod
    def optparser():

        """
        the options function for our parser, it will put everything into play
        """

        parser = argparse.ArgumentParser(
            usage="python autosploit.py -c[z|s|a] -q QUERY [-O|A]\n"
                  "{spacer}[-C WORKSPACE LHOST LPORT] [-e] [--whitewash PATH] [-H]\n"
                  "{spacer}[--ruby-exec] [--msf-path] PATH [-E EXPLOIT-FILE-PATH]\n"
                  "{spacer}[--rand-agent] [--proxy PROTO://IP:PORT] [-P AGENT] [-D QUERY,QUERY,..]".format(
                    spacer=" " * 28
            )
        )
        se = parser.add_argument_group("search engines", "possible search engines to use")
        se.add_argument("-c", "--censys", action="store_true", dest="searchCensys",
                        help="use censys.io as the search engine to gather hosts")
        se.add_argument("-z", "--zoomeye", action="store_true", dest="searchZoomeye",
                        help="use zoomeye.org as the search engine to gather hosts")
        se.add_argument("-s", "--shodan", action="store_true", dest="searchShodan",
                        help="use shodan.io as the search engine to gather hosts")
        se.add_argument("-a", "--all", action="store_true", dest="searchAll",
                        help="search all available search engines to gather hosts")
        save_results_args = se.add_mutually_exclusive_group(required=False)
        save_results_args.add_argument(
            "-O", "--overwrite", action="store_true", dest="overwriteHosts",
            help="When specified, start from scratch by overwriting the host file with new search results."
        )
        save_results_args.add_argument("-A", "--append", action="store_true", dest="appendHosts",
                                       help="When specified, append discovered hosts to the host file.")

        req = parser.add_argument_group("requests", "arguments to edit your requests")
        req.add_argument("--proxy", metavar="PROTO://IP:PORT", dest="proxyConfig",
                         help="run behind a proxy while performing the searches")
        req.add_argument("--random-agent", action="store_true", dest="randomAgent",
                         help="use a random HTTP User-Agent header")
        req.add_argument("-P", "--personal-agent", metavar="USER-AGENT", dest="personalAgent",
                         help="pass a personal User-Agent to use for HTTP requests")
        req.add_argument("-q", "--query", metavar="QUERY", dest="searchQuery",
                         help="pass your search query")

        exploit = parser.add_argument_group("exploits", "arguments to edit your exploits")
        exploit.add_argument("-E", "--exploit-file", metavar="PATH", dest="exploitList",
                             help="provide a text file to convert into JSON and save for later use")
        exploit.add_argument("-C", "--config", nargs=3, metavar=("WORKSPACE", "LHOST", "LPORT"), dest="msfConfig",
                             help="set the configuration for MSF (IE -C default 127.0.0.1 8080)")
        exploit.add_argument("-e", "--exploit", action="store_true", dest="startExploit",
                             help="start exploiting the already gathered hosts")
        exploit.add_argument("-d", "--dry-run", action="store_true", dest="dryRun",
                             help="msfconsole will never be called when this flag is passed")
        exploit.add_argument("-f", "--exploit-file-to-use", metavar="PATH", dest="exploitFile",
                             help="Run AutoSploit with provided exploit JSON file.")
        exploit.add_argument("-H", "--is-honeypot", type=float, default=1000, dest="checkIfHoneypot", metavar="HONEY-SCORE",
                             help="Determine if the host is a honeypot or not")

        misc = parser.add_argument_group("misc arguments", "arguments that don't fit anywhere else")
        misc.add_argument("--ruby-exec", action="store_true", dest="rubyExecutableNeeded",
                          help="if you need to run the Ruby executable with MSF use this")
        misc.add_argument("--msf-path", metavar="MSF-PATH", dest="pathToFramework",
                          help="pass the path to your framework if it is not in your ENV PATH")
        misc.add_argument("--ethics", action="store_true", dest="displayEthics",
                          help=argparse.SUPPRESS)  # easter egg!
        misc.add_argument("--whitelist", metavar="PATH", dest="whitelist",
                          help="only exploit hosts listed in the whitelist file")
        misc.add_argument("-D", "--download", nargs="+", metavar="SEARCH1 SEARCH2 ...", dest="downloadModules",
                          help="download new exploit modules with a provided search flag")
        opts = parser.parse_args()
        return opts

    @staticmethod
    def parse_provided(opt):
        """
        parse the provided arguments to make sure that they are all compatible with one another
        """
        parser = any([opt.searchAll, opt.searchZoomeye, opt.searchCensys, opt.searchShodan])

        if opt.rubyExecutableNeeded and opt.pathToFramework is None:
            lib.settings.close("if the Ruby exec is needed, so is the path to metasploit, pass the `--msf-path` switch")
        if opt.pathToFramework is not None and not opt.rubyExecutableNeeded:
            lib.settings.close(
                "if you need the metasploit path, you also need the ruby executable. pass the `--ruby-exec` switch"
            )
        if opt.personalAgent is not None and opt.randomAgent:
            lib.settings.close("you cannot use both a personal agent and a random agent, choose only one")
        if parser and opt.searchQuery is None:
            lib.settings.close("must provide a search query with the `-q/--query` switch")
        if not parser and opt.searchQuery is not None:
            lib.settings.close(
                "you provided a query and no search engine, choose one with `-s/--shodan/-z/--zoomeye/-c/--censys` "
                "or all with `-a/--all`"
            )
        if opt.startExploit and opt.msfConfig is None:
            lib.settings.close(
                "you must provide the configuration for metasploit in order to start the exploits "
                "do so by passing the `-C\--config` switch (IE -C default 127.0.0.1 8080). don't be "
                "an idiot and keep in mind that sending connections back to your localhost is "
                "probably not a good idea"
            )
        if not opt.startExploit and opt.msfConfig is not None:
            lib.settings.close(
                "you have provided configuration without attempting to exploit, you must pass the "
                "`-e/--exploit` switch to start exploiting"
            )

    @staticmethod
    def single_run_args(opt, keys, loaded_modules):
        """
        run the arguments provided
        """
        api_searches = (
            api_calls.zoomeye.ZoomEyeAPIHook,
            api_calls.shodan.ShodanAPIHook,
            api_calls.censys.CensysAPIHook
        )
        headers = lib.settings.configure_requests(
            proxy=opt.proxyConfig, agent=opt.personalAgent, rand_agent=opt.randomAgent
        )
        single_search_msg = "using {} as the search engine"

        if opt.displayEthics:
            ethics_file = "{}/etc/text_files/ethics.lst".format(os.getcwd())
            with open(ethics_file) as ethics:
                ethic = random.choice(ethics.readlines()).strip()
                lib.settings.close(
                    "You should take this ethical lesson into consideration "
                    "before you continue with the use of this tool:\n\n{}\n".format(ethic))
        if opt.downloadModules is not None:
            import re

            modules_to_download = opt.downloadModules
            links_list = "{}/etc/text_files/links.txt".format(lib.settings.CUR_DIR)
            possibles = open(links_list).readlines()
            for module in modules_to_download:
                searcher = re.compile("{}".format(module))
                for link in possibles:
                    if searcher.search(link) is not None:
                        filename = lib.settings.download_modules(link.strip())
                        download_filename = "{}.json".format(link.split("/")[-1].split(".")[0])
                        download_path = "{}/etc/json".format(os.getcwd())
                        current_files = os.listdir(download_path)
                        if download_filename not in current_files:
                            full_path = "{}/{}".format(download_path, download_filename)
                            lib.jsonize.text_file_to_dict(filename, filename=full_path)
                            lib.output.info("downloaded into: {}".format(download_path))
                        else:
                            lib.output.warning("file already downloaded, skipping")
        if opt.exploitList:
            try:
                lib.output.info("converting {} to JSON format".format(opt.exploitList))
                done = lib.jsonize.text_file_to_dict(opt.exploitList)
                lib.output.info("converted successfully and saved under {}".format(done))
            except IOError as e:
                lib.output.error("caught IOError '{}' check the file path and try again".format(str(e)))
            sys.exit(0)

        search_save_mode = None
        if opt.overwriteHosts:
            # Create a new empty file, overwriting the previous one.
            # Set the mode to append afterwards
            # This way, successive searches will start clean without
            # overriding each others.
            open(lib.settings.HOST_FILE, mode="w").close()
            search_save_mode = "a"
        elif opt.appendHosts:
            search_save_mode = "a"

        # changed my mind it's not to bad
        if opt.searchCensys:
            lib.output.info(single_search_msg.format("Censys"))
            api_searches[2](
                keys["censys"][1], keys["censys"][0],
                opt.searchQuery, proxy=headers[0], agent=headers[1],
                save_mode=search_save_mode
            ).search()
        if opt.searchZoomeye:
            lib.output.info(single_search_msg.format("Zoomeye"))
            api_searches[0](
                opt.searchQuery, proxy=headers[0], agent=headers[1],
                save_mode=search_save_mode
            ).search()
        if opt.searchShodan:
            lib.output.info(single_search_msg.format("Shodan"))
            api_searches[1](
                keys["shodan"][0], opt.searchQuery, proxy=headers[0], agent=headers[1],
                save_mode=search_save_mode
            ).search()
        if opt.searchAll:
            lib.output.info("searching all search engines in order")
            api_searches[0](
                opt.searchQuery, proxy=headers[0], agent=headers[1],
                save_mode=search_save_mode
            ).search()
            api_searches[1](
                keys["shodan"][0], opt.searchQuery, proxy=headers[0], agent=headers[1],
                save_mode=search_save_mode
            ).search()
            api_searches[2](
                keys["censys"][1], keys["censys"][0], opt.searchQuery, proxy=headers[0], agent=headers[1],
                save_mode=search_save_mode
            ).search()
        if opt.startExploit:
            hosts = open(lib.settings.HOST_FILE).readlines()
            if opt.whitelist:
                hosts = lib.exploitation.exploiter.whitelist_wash(hosts, whitelist_file=opt.whitelist)
            if opt.checkIfHoneypot != 1000:
                check_pot = True
            else:
                check_pot = False
            lib.exploitation.exploiter.AutoSploitExploiter(
                opt.msfConfig,
                loaded_modules,
                hosts,
                ruby_exec=opt.rubyExecutableNeeded,
                msf_path=opt.pathToFramework,
                dryRun=opt.dryRun,
                shodan_token=keys["shodan"][0],
                check_honey=check_pot,
                compare_honey=opt.checkIfHoneypot
            ).start_exploit()
