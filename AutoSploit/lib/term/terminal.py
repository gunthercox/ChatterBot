import os
import json
import datetime

import lib.banner
import lib.settings
import lib.output
import lib.errors
import lib.jsonize
import api_calls.shodan
import api_calls.zoomeye
import api_calls.censys
import lib.exploitation.exploiter
try:
    raw_input
except:
    input = raw_input


class AutoSploitTerminal(object):

    """
    class object for the main terminal of the program
    """

    internal_terminal_commands = [
        # viewing gathered hosts
        "view", "show",
        # displaying memory
        "mem", "memory", "history",
        # attacking targets
        "exploit", "run", "attack",
        # search API's
        "search", "api", "gather",
        # quit the terminal
        "exit", "quit",
        # single hosts
        "single",
        # custom hosts list
        "custom", "personal",
        # display help
        "?", "help",
        # display external commands
        "external",
        # reset API tokens
        "reset", "tokens",
        # show the version number
        "ver", "version",
        # clean the hosts file of duplicate IP's
        "clean", "clear",
        # easter eggs!
        "idkwhatimdoing", "ethics", "skid",
        # nmap arguments
        "nmap", "mapper", "mappy"
    ]
    external_terminal_commands = lib.settings.load_external_commands()
    api_call_pointers = {
        "shodan": api_calls.shodan.ShodanAPIHook,
        "zoomeye": api_calls.zoomeye.ZoomEyeAPIHook,
        "censys": api_calls.censys.CensysAPIHook
    }

    def __init__(self, tokens, modules):
        self.history = []
        self.quit_terminal = False
        self.tokens = tokens
        self.history_dir = "{}/{}".format(lib.settings.HISTORY_FILE_PATH, datetime.date.today())
        self.full_history_path = "{}/autosploit.history".format(self.history_dir)
        self.modules = modules
        try:
            self.loaded_hosts = open(lib.settings.HOST_FILE).readlines()
        except (IOError, Exception):
            lib.output.warning("no hosts file present")
            self.loaded_hosts = open(lib.settings.HOST_FILE, "a+").readlines()

    def __reload(self):
        self.loaded_hosts = open(lib.settings.HOST_FILE).readlines()

    def reflect_memory(self, max_memory=100):
        """
        reflect the command memory out of the history file
        """
        if os.path.exists(self.history_dir):
            tmp = []
            try:
                with open(self.full_history_path) as history:
                    for item in history.readlines():
                        tmp.append(item.strip())
            except:
                pass
            if len(tmp) == 0:
                lib.output.warning("currently no history")
            elif len(tmp) > max_memory:
                import shutil

                history_file_backup_path = "{}.{}.old".format(
                    self.full_history_path,
                    lib.jsonize.random_file_name(length=12)
                )
                shutil.copy(self.full_history_path, history_file_backup_path)
                os.remove(self.full_history_path)
                open(self.full_history_path, 'a+').close()
                lib.output.misc_info("history file to large, backed up under '{}'".format(history_file_backup_path))
            else:
                for cmd in tmp:
                    self.history.append(cmd)

    def do_display_history(self):
        """
        display the history from the history files
        """
        for i, item in enumerate(self.history, start=1):
            if len(list(str(i))) == 2:
                spacer1, spacer2 = "  ", "   "
            elif len(list(str(i))) == 3:
                spacer1, spacer2 = " ", "   "
            else:
                spacer1, spacer2 = "   ", "   "
            print("{}{}{}{}".format(spacer1, i, spacer2, item))

    def get_choice(self):
        """
        get the provided choice and return a tuple of options and the choice
        """
        original_choice = raw_input(lib.settings.AUTOSPLOIT_PROMPT)
        try:
            choice_checker = original_choice.split(" ")[0]
        except:
            choice_checker = original_choice
        if choice_checker in self.internal_terminal_commands:
            retval = ("internal", original_choice)
        elif choice_checker in self.external_terminal_commands:
            retval = ("external", original_choice)
        else:
            retval = ("unknown", original_choice)
        return retval

    def do_show_version_number(self):
        """
        display the current version number
        """
        lib.output.info("your current version number: {}".format(lib.banner.VERSION))

    def do_display_external(self):
        """
        display all external commands
        """
        print(" ".join(self.external_terminal_commands))

    def do_terminal_command(self, command):
        """
        run a terminal command
        """
        lib.settings.cmdline(command, is_msf=False)

    def do_clean_hosts(self):
        """
        Clean the hosts.txt file of any duplicate IP addresses
        """
        retval = set()
        current_size = len(self.loaded_hosts)
        for host in self.loaded_hosts:
            retval.add(host)
        cleaned_size = len(retval)
        with open(lib.settings.HOST_FILE, 'w') as hosts:
            for item in list(retval):
                hosts.write(item)
        if current_size != cleaned_size:
            lib.output.info("cleaned {} duplicate IP address(es) (total of {})".format(
                current_size - cleaned_size, cleaned_size
            )
            )
        self.__reload()

    def do_token_reset(self, api, token, username):
        """
        Explanation:
        ------------
        Reset the API tokens when needed, this will overwrite the existing
        API token with a provided one

        Parameters:
        -----------
        :param api: name of the API to reset
        :param token: the token that will overwrite the current token
        :param username: if resetting Censys this will be the user ID token

        Examples:
        ---------
        Censys ->  reset/tokens censys <token> <userID>
        Shodan ->  reset.tokens shodan <token>
        """
        import sys

        if sys.version_info > (3,):
            token = token.encode("utf-8")
            username = username.encode("utf-8")

        if api.lower() == "censys":
            lib.output.info("resetting censys API credentials")
            with open(lib.settings.API_KEYS["censys"][0], 'w') as token_:
                token_.write(token)
            with open(lib.settings.API_KEYS["censys"][1], 'w') as username_:
                username_.write(username)
        else:
            with open(lib.settings.API_KEYS["shodan"][0], 'w') as token_:
                token_.write(token)
        lib.output.warning("program must be restarted for the new tokens to initialize")

    def do_api_search(self, requested_api_data, query, tokens):
        """
        Explanation:
        ------------
        Search the API with a provided query for potentially exploitable hosts.

        Parameters:
        -----------
        :param requested_api_data: data to be used with the API tuple of info
        :param query: the query to be searched
        :param tokens: an argument dict that will contain the token information

        Command Format:
        --------------
        search[/api/gather] API_NAME[API_NAME,...](shodan,censys,zoomeye) QUERY

        Examples:
        ---------
        search shodan,censys,zoomeye windows 10
        search shodan windows 7
        """
        acceptable_api_names = ("shodan", "censys", "zoomeye")
        api_checker = lambda l: all(i.lower() in acceptable_api_names for i in l)

        try:
            if len(query) < 1:
                query = "".join(query)
            else:
                query = " ".join(query)
        except:
            query = query

        if query == "" or query.isspace():
            lib.output.warning("looks like you forgot the query")
            return
        try:
            api_list = requested_api_data.split(",")
        except:
            api_list = [requested_api_data]
        prompt_for_save = len(open(lib.settings.HOST_FILE).readlines()) != 0
        if prompt_for_save:
            save_mode = lib.output.prompt(
                "would you like to [a]ppend or [o]verwrite the file[a/o]", lowercase=True
            )
            if save_mode.startswith("o"):
                backup = lib.settings.backup_host_file(lib.settings.HOST_FILE, lib.settings.HOST_FILE_BACKUP)
                lib.output.misc_info("current host file backed up under: '{}'".format(backup))
                save_mode = "w"
            else:
                if not any(save_mode.startswith(s) for s in ("a", "o")):
                    lib.output.misc_info("provided option is not valid, defaulting to 'a'")
                    save_mode = "a+"
        else:
            save_mode = "a+"

        proxy = lib.output.prompt("enter your proxy or press enter for none", lowercase=False)
        if proxy.isspace() or proxy == "":
            proxy = {"http": "", "https": ""}
        else:
            proxy = {"http": proxy, "https": proxy}
        agent = lib.output.prompt("use a [r]andom User-Agent or the [d]efault one[r/d]", lowercase=True)
        if agent.startswith("r"):
            agent = {"User-Agent": lib.settings.grab_random_agent()}
        elif agent.startswith("d"):
            agent = {"User-Agent": lib.settings.DEFAULT_USER_AGENT}
        else:
            lib.output.warning("invalid option, using default")
            agent = {"User-Agent": lib.settings.DEFAULT_USER_AGENT}
        for api in api_list:
            res = api_checker([api])
            if not res:
                lib.output.error(
                    "API: '{}' is not a valid API, will be skipped".format(api)
                )
            else:
                with open(lib.settings.QUERY_FILE_PATH, "a+") as tmp:
                    tmp.write(query)
                lib.output.info(
                    "starting search on API {} using query: '{}'".format(api, query)
                )
                try:
                    self.api_call_pointers[api.lower()](
                        token=tokens["shodan"][0] if api == "shodan" else tokens["censys"][0],
                        identity=tokens["censys"][1] if api == "censys" else "",
                        query=query,
                        save_mode=save_mode,
                        proxy=proxy,
                        agent=agent
                    ).search()
                except (lib.errors.AutoSploitAPIConnectionError, Exception) as e:
                    lib.settings.stop_animation = True
                    lib.output.error("error searching API: '{}', error message: '{}'".format(api, str(e)))
        lib.settings.stop_animation = True

    def do_display_usage(self):
        """
        display the full help menu
        """
        print(lib.settings.TERMINAL_HELP_MESSAGE)

    def do_view_gathered(self):
        """
        view the gathered hosts
        """
        if len(self.loaded_hosts) != 0:
            for host in self.loaded_hosts:
                lib.output.info(host.strip())
        else:
            lib.output.warning("currently no gathered hosts")

    def do_add_single_host(self, ip):
        """
        Explanation:
        ------------
        Add a single host by IP address
        Or a list of single hosts separatedd by a comma

        Parameters:
        -----------
        :param ip: IP address to be added

        Command Format:
        --------------
        single IP[,IP,IP,IP,IP,...]

        Examples:
        ---------
        single 89.76.12.124,89.76.12.43
        """
        for item in ip.split(","):
            validated_ip = lib.settings.validate_ip_addr(item)
            if not validated_ip:
                lib.output.error("provided IP '{}' is invalid, try again".format(ip))
            else:
                with open(lib.settings.HOST_FILE, "a+") as hosts:
                    hosts.write(item + "\n")
                    lib.output.info("host '{}' saved to hosts file".format(item))

    def do_quit_terminal(self, save_history=True):
        """
        quit the terminal and save the command history
        """
        self.quit_terminal = True
        if save_history:
            if not os.path.exists(self.history_dir):
                os.makedirs(self.history_dir)
            lib.output.misc_info("saving history")
            with open(self.full_history_path, "a+") as hist:
                for item in self.history:
                    hist.write(item + "\n")
        lib.output.info("exiting terminal session")

    def do_exploit_targets(self, workspace_info, shodan_token=None):
        """
        Explanation:
        ------------
        Exploit the already gathered hosts inside of the hosts.txt file

        Parameters:
        -----------
        :param workspace_info: a tuple of workspace information

        Command Format:
        --------------
        exploit[/run/attack] IP PORT WORKSPACE_NAME [whitewash list]

        Examples:
        ---------
        exploit 127.0.0.1 9065 default whitelist.txt
        """
        if workspace_info[3] is not None and workspace_info[3] != "honeycheck":
            lib.output.misc_info("doing whitewash on hosts file")
            lib.exploitation.exploiter.whitelist_wash(
                open(lib.settings.HOST_FILE).readlines(),
                workspace_info[3]
            )
        else:
            if not lib.settings.check_for_msf():
                msf_path = lib.output.prompt(
                    "metasploit is not in your PATH, provide the full path to it", lowercase=False
                )
                ruby_exec = True
            else:
                msf_path = None
                ruby_exec = False

            sort_mods = lib.output.prompt(
                "sort modules by relevance to last query[y/N]", lowercase=True
            )

            try:
                if sort_mods.lower().startswith("y"):
                    mods_to_use = lib.exploitation.exploiter.AutoSploitExploiter(
                        None, None
                    ).sort_modules_by_query()
                else:
                    mods_to_use = self.modules
            except Exception:
                lib.output.error("error sorting modules defaulting to all")
                mods_to_use = self.modules

            view_modules = lib.output.prompt("view sorted modules[y/N]", lowercase=True)
            if view_modules.startswith("y"):
                for mod in mods_to_use:
                    lib.output.misc_info(mod.strip())
            lib.output.prompt("press enter to start exploitation phase")
            lib.output.info("starting exploitation phase")
            lib.exploitation.exploiter.AutoSploitExploiter(
                configuration=workspace_info[0:3],
                all_modules=mods_to_use,
                hosts=open(lib.settings.HOST_FILE).readlines(),
                msf_path=msf_path,
                ruby_exec=ruby_exec,
                check_honey=workspace_info[-1],
                shodan_token=shodan_token
            ).start_exploit()

    def do_load_custom_hosts(self, file_path):
        """
        Explanation:
        -----------
        Load a custom exploit file, this is useful to attack already gathered hosts
        instead of trying to gather them again from the backup host files inside
        of the `.autosploit_home` directory

        Parameters:
        -----------
        :param file_path: the full path to the loadable hosts file

        Command Format:
        --------------
        custom[/personal] FILE_PATH

        Examples:
        ---------
        custom /some/path/to/myfile.txt
        """
        import shutil

        try:
            open("{}".format(file_path)).close()
        except IOError:
            lib.output.error("file does not exist, check the path and try again")
            return
        lib.output.warning("overwriting hosts file with provided, and backing up current")
        backup_path = lib.settings.backup_host_file(lib.settings.HOST_FILE, lib.settings.HOST_FILE_BACKUP)
        shutil.copy(file_path, lib.settings.HOST_FILE)
        lib.output.info("host file replaced, backup stored under '{}'".format(backup_path))
        self.loaded_hosts = open(lib.settings.HOST_FILE).readlines()

    def do_nmap_scan(self, target, arguments):
        """
        Explanation:
        -----------
        Perform a nmap scan on a provided target, given that nmap is on your system.
        If nmap is not on your system, this will not work, you may also provide
        arguments known to nmap.

        Parameters:
        ----------
        :param target: the target to attack
        :param arguments: a string of arguments separated by a comma

        Command Format:
        --------------
        nmap[/mapper/mappy] TARGET [ARGUMENTS]

        Examples:
        --------
        nmap/mapper/mappy 10.0.1.1 -sV,--dns-servers 1.1.1.1,--reason,-A
        nmap 10.0.1.1/24
        """
        import lib.scanner.nmap

        sep = "-" * 30
        if arguments is not None:
            arguments = arguments.split(",")
            passable_arguments = lib.scanner.nmap.parse_nmap_args(arguments)
        else:
            passable_arguments = None
        try:
            nmap_path = lib.scanner.nmap.find_nmap(lib.settings.NMAP_POSSIBLE_PATHS)
        except lib.errors.NmapNotFoundException:
            nmap_path = None
            lib.output.error("nmap was not found on your system please install nmap first")
            return
        lib.output.info("performing nmap scan on {}".format(target))
        try:
            output, warnings, errors = lib.scanner.nmap.do_scan(target, nmap_path, arguments=passable_arguments)
            formatted_results_output = lib.scanner.nmap.parse_xml_output(output, warnings, errors)
            save_file = lib.scanner.nmap.write_data(target, formatted_results_output, is_xml=False)
            lib.output.misc_info("JSON data dumped to file: '{}'".format(save_file))
            print("{sep}\n{data}\n{sep}".format(
                data=json.dumps(formatted_results_output["nmap_scan"][target], indent=4), sep=sep
            ))
        except lib.errors.NmapScannerError as e:
            lib.output.error(str(e).strip())

    def terminal_main_display(self, tokens, extra_commands=None, save_history=True):
        # idk what the fuck the problem is but this seems to fix it so...
        import lib.output
        """
        terminal main display
        """
        lib.output.warning(
            "no arguments have been parsed at run time, dropping into terminal session. "
            "to get help type `help` to quit type `exit/quit` to get help on "
            "a specific command type `command help`"
        )

        if extra_commands is not None:
            for command in extra_commands:
                self.external_terminal_commands.append(command)
        self.reflect_memory()
        while not self.quit_terminal:
            try:
                lib.settings.auto_completer(self.internal_terminal_commands)
                try:
                    choice_type, choice = self.get_choice()
                    if choice_type == "unknown":
                        sims = lib.settings.find_similar(
                            choice,
                            self.internal_terminal_commands,
                            self.external_terminal_commands
                        )
                        if len(sims) != 0:
                            max_sims_display = 7
                            print(
                                "no command '{}' found, but there {} {} similar command{}".format(
                                    choice,
                                    "are" if len(sims) > 1 else "is",
                                    len(sims),
                                    "s" if len(sims) > 1 else ""
                                )
                            )
                            if len(sims) > max_sims_display:
                                print("will only display top {} results".format(max_sims_display))
                            for i, cmd in enumerate(sims, start=1):
                                if i == max_sims_display:
                                    break
                                print(cmd)
                            print("{}: command not found".format(choice))
                        else:
                            print("{} command not found".format(choice))
                        self.history.append(choice)
                    elif choice_type == "external":
                        self.do_terminal_command(choice)
                        self.history.append(choice)
                    else:
                        try:
                            choice_data_list = choice.split(" ")
                            if choice_data_list[-1] == "":
                                choice_data_list = None
                        except:
                            choice_data_list = None
                        if choice == "?" or choice == "help":
                            self.do_display_usage()
                        elif any(c in choice for c in ("external",)):
                            self.do_display_external()
                        elif any(c in choice for c in ("history", "mem", "memory")):
                            self.do_display_history()
                        elif any(c in choice for c in ("exit", "quit")):
                            self.do_quit_terminal(save_history=save_history)
                        elif any(c in choice for c in ("view", "show")):
                            self.do_view_gathered()
                        elif any(c in choice for c in ("version",)):
                            self.do_show_version_number()
                        elif any(c in choice for c in ("clean", "clear")):
                            self.do_clean_hosts()
                        elif "single" in choice:
                            try:
                                if "help" in choice_data_list:
                                    print(self.do_load_custom_hosts.__doc__)
                            except TypeError:
                                pass
                            if choice_data_list is None or len(choice_data_list) == 1:
                                lib.output.error("must provide host IP after `single` keyword (IE single 89.65.78.123)")
                            else:
                                self.do_add_single_host(choice_data_list[-1])
                        elif any(c in choice for c in ("exploit", "run", "attack")):
                            try:
                                if "help" in choice_data_list:
                                    print(self.do_exploit_targets.__doc__)
                            except TypeError:
                                pass
                            if choice_data_list is None or len(choice_data_list) < 4:
                                lib.output.error(
                                    "must provide at least LHOST, LPORT, workspace name with `{}` keyword "
                                    "(IE {} 127.0.0.1 9076 default [whitelist-path] [honeycheck])".format(
                                        choice.split(" ")[0].strip(), choice.split(" ")[0].strip()
                                    )
                                )
                            else:
                                if lib.settings.validate_ip_addr(choice_data_list[1], home_ok=True):
                                    try:
                                        workspace = (
                                            choice_data_list[1], choice_data_list[2],
                                            choice_data_list[3], choice_data_list[4],
                                            True if "honeycheck" in choice_data_list else False
                                        )
                                    except IndexError:
                                        workspace = (
                                            choice_data_list[1], choice_data_list[2],
                                            choice_data_list[3], None,
                                            True if "honeycheck" in choice_data_list else False
                                        )
                                    if workspace[-1]:
                                        honeyscore = None
                                        while honeyscore is None:
                                            honeyscore = lib.output.prompt(
                                                "enter the honeyscore you want as the maximum allowed"
                                            )
                                            try:
                                                honeyscore = float(honeyscore)
                                            except:
                                                honeyscore = None
                                                lib.output.error("honey score must be a float (IE 0.3)")
                                    self.do_exploit_targets(
                                        workspace, shodan_token=self.tokens["shodan"][0]
                                    )
                                else:
                                    lib.output.warning(
                                        "heuristics could not validate provided IP address, "
                                        "did you type it right?"
                                    )
                        elif any(c in choice for c in ("personal", "custom")):
                            try:
                                if "help" in choice_data_list:
                                    print(self.do_load_custom_hosts.__doc__)
                            except TypeError:
                                pass
                            if choice_data_list is not None and len(choice_data_list) == 1:
                                lib.output.error("must provide full path to file after `{}` keyword".format(choice))
                            else:
                                self.do_load_custom_hosts(choice_data_list[-1])
                        elif any(c in choice for c in ("search", "api", "gather")):
                            try:
                                if "help" in choice_data_list:
                                    print(self.do_load_custom_hosts.__doc__)
                            except TypeError:
                                pass
                            if choice_data_list is None or len(choice_data_list) < 3:
                                lib.output.error(
                                    "must provide a list of API names after `{}` keyword and query "
                                    "(IE {} shodan,censys apache2)".format(
                                        choice.split(" ")[0].strip(), choice.split(" ")[0].strip()
                                    )
                                )
                            else:
                                self.do_api_search(choice_data_list[1], choice_data_list[2:], tokens)
                        elif any(c in choice for c in ("idkwhatimdoing", "ethics", "skid")):
                            import random

                            if choice == "ethics" or choice == "idkwhatimdoing":
                                ethics_file = "{}/etc/text_files/ethics.lst".format(os.getcwd())
                                other_file = "{}/etc/text_files/gen".format(os.getcwd())
                                with open(ethics_file) as ethics:
                                    ethic = random.choice(ethics.readlines()).strip()
                                    lib.output.info("take this ethical lesson into consideration before proceeding:")
                                    print("\n{}\n".format(ethic))
                                lib.output.warning(open(other_file).read())
                            else:
                                lib.output.warning("hack to learn, don't learn to hack")
                        elif any(c in choice for c in ("tokens", "reset")):
                            acceptable_api_names = ("shodan", "censys")

                            try:
                                if "help" in choice_data_list:
                                    print(self.do_load_custom_hosts.__doc__)
                            except TypeError:
                                pass

                            if choice_data_list is None or len(choice_data_list) < 3:
                                lib.output.error(
                                    "must supply API name with `{}` keyword along with "
                                    "new token (IE {} shodan mytoken123 [userID (censys)])".format(
                                        choice.split(" ")[0].strip(), choice.split(" ")[0].strip()
                                    )
                                )
                            else:
                                if choice_data_list[1].lower() in acceptable_api_names:
                                    try:
                                        api, token, username = choice_data_list[1], choice_data_list[2], choice_data_list[3]
                                    except IndexError:
                                        api, token, username = choice_data_list[1], choice_data_list[2], None
                                    self.do_token_reset(api, token, username)
                                else:
                                    lib.output.error("cannot reset {} API credentials".format(choice))
                        elif any(c in choice for c in ["nmap", "mapper", "mappy"]):
                            try:
                                if "help" in choice_data_list:
                                    print(self.do_nmap_scan.__doc__)
                            except TypeError:
                                pass
                            target = choice_data_list[1]
                            try:
                                arguments = choice_data_list[2]
                                lib.output.warning(
                                    "arguments that have a space in them most likely will not be processed correctly, "
                                    "(IE --dns-servers 1.1.1.1 will most likely cause issues)"
                                )
                            except IndexError:
                                arguments = None
                            # don't know how im going to implement ports yet
                            # try:
                            #     ports = choice_data_list[3]
                            # except IndexError:
                            #     ports = None
                            if "help" not in choice_data_list:
                                self.do_nmap_scan(target, arguments)
                        self.history.append(choice)
                        self.__reload()
                except KeyboardInterrupt:
                    lib.output.warning("use the `exit/quit` command to end terminal session")
            except IndexError:
                pass
            except Exception as e:
                global stop_animation

                stop_animation = True

                import sys
                import traceback
                import lib.creation.issue_creator

                print(
                    "\033[31m[!] AutoSploit has hit an unhandled exception: '{}', "
                    "in order for the developers to troubleshoot and repair the "
                    "issue AutoSploit will need to gather your OS information, "
                    "current arguments, the error message, and a traceback. "
                    "None of this information can be used to identify you in any way\033[0m".format(str(e))
                )
                error_traceback = ''.join(traceback.format_tb(sys.exc_info()[2]))
                error_class = str(e.__class__).split(" ")[1].split(".")[1].strip(">").strip("'")
                error_file = lib.settings.save_error_to_file(str(error_traceback), str(e), error_class)
                lib.creation.issue_creator.request_issue_creation(error_file, lib.creation.issue_creator.hide_sensitive(), str(e))
                lib.output.info("continuing terminal session")
                # this way if you're in the terminal already we won't quit out of it
                continue
