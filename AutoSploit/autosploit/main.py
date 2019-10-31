import os
import sys
import ctypes
import psutil
import platform

from lib.cmdline.cmd import AutoSploitParser
from lib.term.terminal import AutoSploitTerminal
from lib.creation.issue_creator import (
    request_issue_creation,
    hide_sensitive
)
from lib.output import (
    info,
    prompt,
    misc_info
)
from lib.settings import (
    logo,
    load_api_keys,
    check_services,
    cmdline,
    close,
    EXPLOIT_FILES_PATH,
    START_SERVICES_PATH,
    save_error_to_file,
    stop_animation
)
from lib.jsonize import (
    load_exploits,
    load_exploit_file
)


def main():
    try:

        try:
            is_admin = os.getuid() == 0
        except AttributeError:
            # we'll make it cross platform because it seems like a cool idea
            is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0

        if not is_admin:
            close("must have admin privileges to run")

        opts = AutoSploitParser().optparser()

        logo()
        info("welcome to autosploit, give us a little bit while we configure")
        misc_info("checking your running platform")
        platform_running = platform.system()
        misc_info("checking for disabled services")
        # according to ps aux, postgre and apache2 are the names of the services on Linux systems
        service_names = ("postgres", "apache2")
        try:
            for service in list(service_names):
                while not check_services(service):
                    if "darwin" in platform_running.lower():
                        info(
                            "seems you're on macOS, skipping service checks "
                            "(make sure that Apache2 and PostgreSQL are running)"
                        )
                        break
                    choice = prompt(
                        "it appears that service {} is not enabled, would you like us to enable it for you[y/N]".format(
                            service.title()
                        )
                    )
                    if choice.lower().startswith("y"):
                        try:
                            if "linux" in platform_running.lower():
                                cmdline("{} linux".format(START_SERVICES_PATH))
                            else:
                                close("your platform is not supported by AutoSploit at this time", status=2)

                            # moving this back because it was funky to see it each run
                            info("services started successfully")
                        # this tends to show up when trying to start the services
                        # I'm not entirely sure why, but this fixes it
                        except psutil.NoSuchProcess:
                            pass
                    else:
                        process_start_command = "`sudo service {} start`"
                        if "darwin" in platform_running.lower():
                            process_start_command = "`brew services start {}`"
                        close(
                            "service {} is required to be started for autosploit to run successfully (you can do it manually "
                            "by using the command {}), exiting".format(
                                service.title(), process_start_command.format(service)
                            )
                        )
        except Exception:
            pass

        if len(sys.argv) > 1:
            info("attempting to load API keys")
            loaded_tokens = load_api_keys()
            AutoSploitParser().parse_provided(opts)

            if not opts.exploitFile:
                misc_info("checking if there are multiple exploit files")
                loaded_exploits = load_exploits(EXPLOIT_FILES_PATH)
            else:
                loaded_exploits = load_exploit_file(opts.exploitFile)
                misc_info("Loaded {} exploits from {}.".format(
                    len(loaded_exploits),
                    opts.exploitFile))

            AutoSploitParser().single_run_args(opts, loaded_tokens, loaded_exploits)
        else:
            misc_info("checking if there are multiple exploit files")
            loaded_exploits = load_exploits(EXPLOIT_FILES_PATH)
            info("attempting to load API keys")
            loaded_tokens = load_api_keys()
            terminal = AutoSploitTerminal(loaded_tokens, loaded_exploits)
            terminal.terminal_main_display(loaded_tokens)
    except Exception as e:
        global stop_animation

        stop_animation = True

        import traceback

        print(
            "\033[31m[!] AutoSploit has hit an unhandled exception: '{}', "
            "in order for the developers to troubleshoot and repair the "
            "issue AutoSploit will need to gather your OS information, "
            "current arguments, the error message, and a traceback. "
            "None of this information can be used to identify you in any way\033[0m".format(str(e))
        )
        error_traceback = ''.join(traceback.format_tb(sys.exc_info()[2]))
        error_class = str(e.__class__).split(" ")[1].split(".")[1].strip(">").strip("'")
        error_file = save_error_to_file(str(error_traceback), str(e), error_class)
        print error_traceback
        # request_issue_creation(error_file, hide_sensitive(), str(e))
