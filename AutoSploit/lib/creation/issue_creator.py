import re
import os
import sys
import json
import platform
import hashlib
import base64
try:
    from urllib2 import Request, urlopen
except ImportError:
    from urllib.request import Request, urlopen

import requests
from bs4 import BeautifulSoup

import lib.settings
import lib.output
import lib.banner

try:
    raw_input
except NameError:
    raw_input = input


def checksum(issue_template_path):
    """
    verifies the checksums of the program before you can create an issue
    """

    file_skips = [
        "__init__", ".pyc", ".xml",
        ".sample", "HEAD", "pack",
        "dev-beta", "description", "config",
        "exclude", "index", ".json",
        ".gitignore", "LICENSE", "ISSUE_TEMPLATE",
        "README", "CONTRIBUTING", "hosts.txt",
        "requirements.txt", "checksum_link.txt",
        ".key", ".id", ".csv"
    ]
    current_checksums = []
    failed_checks = 0
    for root, sub, files in os.walk(lib.settings.CUR_DIR):
        for name in files:
            if not any(c in name for c in file_skips):
                path = os.path.join(root, name)
                check = hashlib.md5()
                check.update(open(path).read())
                check = check.hexdigest()
                current_checksums.append("{}:{}".format(path.split("/")[-1], check))
    try:
        req = requests.get(lib.settings.CHECKSUM_LINK)
        real_checksums = str(req.text).split("\n")
        for real, current in zip(sorted(real_checksums), sorted(current_checksums)):
            if real != current:
                failed_checks += 1
        if failed_checks > 0:
            return False
        return True
    except Exception:
        sep = "-" * 35
        lib.output.error(
            "something went wrong while verifying the checksums of the current application, "
            "this could be due to your internet connectivity. Please either try again, or use "
            "the following template to create an issue:"
        )
        print("{}\n{}\n{}".format(
            sep, open(issue_template_path).read(), sep
        ))
        exit(1)


def check_version_number(current_version):
    """
    check the version number before creating an issue
    """
    version_checker = re.compile(r"version.=.\S\d.\d.(\d)?", re.I)
    try:
        req = requests.get("https://raw.githubusercontent.com/NullArray/AutoSploit/master/lib/banner.py")
        available_version = version_checker.search(req.content).group().split("=")[-1].split('"')[1]
        if available_version > current_version:
            return False
        return True
    except Exception:
        return True


def create_identifier(data):
    """
    create the exception identifier
    """
    obj = hashlib.sha1()
    try:
        obj.update(data)
    except:
        obj.update(data.encode("utf-8"))
    return obj.hexdigest()[1:10]


def get_token(path):
    """
    we know what this is for
    """
    with open(path) as _token:
        data = _token.read()
        token, n = data.split(":")
        for _ in range(int(n)):
            token = base64.b64decode(token)
    return token


def ensure_no_issue(param):
    """
    ensure that there is not already an issue that has been created for yours
    """
    urls = (
        "https://github.com/NullArray/AutoSploit/issues",
        "https://github.com/NullArray/AutoSploit/issues?q=is%3Aissue+is%3Aclosed"
    )
    for url in urls:
        req = requests.get(url)
        param = re.compile(param)
        try:
            if param.search(req.content) is not None:
                return True
        except:
            content = str(req.content)
            if param.search(content) is not None:
                return True
    return False


def find_url(params):
    """
    get the URL that your issue is created at
    """
    searches = (
        "https://github.com/NullArray/AutoSploit/issues",
        "https://github.com/NullArray/AutoSploit/issues?q=is%3Aissue+is%3Aclosed"
    )
    for search in searches:
        retval = "https://github.com{}"
        href = None
        searcher = re.compile(params, re.I)
        req = requests.get(search)
        status, html = req.status_code, req.content
        if status == 200:
            split_information = str(html).split("\n")
            for i, line in enumerate(split_information):
                if searcher.search(line) is not None:
                    href = split_information[i]
        if href is not None:
            soup = BeautifulSoup(href, "html.parser")
            for item in soup.findAll("a"):
                link = item.get("href")
                return retval.format(link)
    return None


def hide_sensitive():
    """
    hide sensitive information from the terminal
    """
    sensitive = (
        "--proxy", "-P", "--personal-agent", "-q", "--query", "-C", "--config",
        "--whitelist", "--msf-path"
    )
    args = sys.argv
    for item in sys.argv:
        if item in sensitive:
            if item in ["-C", "--config"]:
                try:
                    item_index = args.index("-C") + 1
                except ValueError:
                    item_index = args.index("--config") + 1
                for _ in range(3):
                    hidden = ''.join([x.replace(x, '*') for x in str(args[item_index])])
                    args.pop(item_index+_)
                    args.insert(item_index, hidden)
                return ' '.join(args)
            else:
                try:
                    item_index = args.index(item) + 1
                    hidden = ''.join([x.replace(x, "*") for x in str(args[item_index])])
                    args.pop(item_index)
                    args.insert(item_index, hidden)
                    return ' '.join(args)
                except:
                    return ' '.join([item for item in sys.argv])


def request_issue_creation(path, arguments, error_message):
    """
    request the creation and create the issue
    """

    # TODO:/ we're gonna go ahead and give you guys another chance
    #if not checksum(path):
    #    lib.output.error(
    #        "It seems you have changed some of the code in the program. We do not accept issues from edited "
    #        "code as we have no way of reliably testing your issue. We recommend that you only use the version "
    #        "that is available on github, no issue will be created for this problem."
    #    )
    #    exit(1)

    question = raw_input(
        "do you want to create an anonymized issue?[y/N]: "
    )
    if question.lower().startswith("y"):
        if check_version_number(lib.banner.VERSION):
            # gonna read a chunk of it instead of one line
            chunk = 4096
            with open(path) as data:
                identifier = create_identifier(error_message)
                # gotta seek to the beginning of the file since it's already been read `4096` into it
                data.seek(0)
                issue_title = "Unhandled Exception ({})".format(identifier)

            issue_data = {
                "title": issue_title,
                "body": (
                    "Autosploit version: `{}`\n"
                    "OS information: `{}`\n"
                    "Running context: `{}`\n"
                    "Error mesage: `{}`\n"
                    "Error traceback:\n```\n{}\n```\n"
                    "Metasploit launched: `{}`\n".format(
                        lib.banner.VERSION,
                        platform.platform(),
                        ' '.join(sys.argv),
                        error_message,
                        open(path).read(),
                        lib.settings.MSF_LAUNCHED,
                    )
                )
            }

            _json_data = json.dumps(issue_data)
            if sys.version_info > (3,):  # python 3
                _json_data = _json_data.encode("utf-8")

            if not ensure_no_issue(identifier):
                req = Request(
                    url="https://api.github.com/repos/nullarray/autosploit/issues", data=_json_data,
                    headers={"Authorization": "token {}".format(get_token(lib.settings.TOKEN_PATH))}
                )
                urlopen(req, timeout=10).read()
                lib.output.info(
                    "issue has been generated with the title '{}', at the following "
                    "URL '{}'".format(
                        issue_title, find_url(identifier)
                    )
                )
            else:
                lib.output.error(
                    "someone has already created this issue here: {}".format(find_url(identifier))
                )
            try:
                os.remove(path)
            except:
                pass
        else:
            sep = "-" * 35
            lib.output.error(
                "it appears you are not using the current version of AutoSploit please update to the newest version "
                "and try again, this can also happen when a new update has been pushed and the cached raw page has "
                "not been updated yet. If you feel this is the later please create and issue on AutoSploits Github "
                "page with the following info:"
            )
            print("{}\n{}\n{}".format(sep, open(path).read(), sep))
    else:
        lib.output.info("the issue has been logged to a file in path: '{}'".format(path))
