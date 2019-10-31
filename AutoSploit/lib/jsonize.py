import os
import json
import string
import random

import lib.output
import lib.settings


def random_file_name(acceptable=string.ascii_letters, length=7):
    """
    create a random filename.

     `note: this could potentially cause issues if there
           a lot of files in the directory`
    """
    retval = set()
    for _ in range(length):
        retval.add(random.choice(acceptable))
    return ''.join(list(retval))


def load_exploit_file(path, node="exploits"):
    """
    load exploits from a given file
    """
    selected_file_path = path

    retval = []
    try:
        with open(selected_file_path) as exploit_file:
            # loading it like this has been known to cause Unicode issues later on down
            # the road
            _json = json.loads(exploit_file.read())
            for item in _json[node]:
                # so we'll reload it into a ascii string before we save it into the file
                retval.append(str(item))
    except IOError as e:
        lib.settings.close(e)
    return retval


def load_exploits(path, node="exploits"):
    """
    load exploits from a given path, depending on how many files are loaded into
    the beginning `file_list` variable it will display a list of them and prompt
    or just select the one in the list
    """
    retval = []
    file_list = os.listdir(path)
    selected = False
    if len(file_list) != 1:
        lib.output.info("total of {} exploit files discovered for use, select one:".format(len(file_list)))
        while not selected:
            for i, f in enumerate(file_list, start=1):
                print("{}. '{}'".format(i, f[:-5]))
            action = raw_input(lib.settings.AUTOSPLOIT_PROMPT)
            try:
                selected_file = file_list[int(action) - 1]
                selected = True
            except Exception:
                lib.output.warning("invalid selection ('{}'), select from below".format(action))
                selected = False
    else:
        selected_file = file_list[0]

    selected_file_path = os.path.join(path, selected_file)

    with open(selected_file_path) as exploit_file:
        # loading it like this has been known to cause Unicode issues later on down
        # the road
        _json = json.loads(exploit_file.read())
        for item in _json[node]:
            # so we'll reload it into a ascii string before we save it into the file
            retval.append(str(item))
    return retval


def text_file_to_dict(path, filename=None):
    """
    take a text file path, and load all of the information into a `dict`
    send that `dict` into a JSON format and save it into a file. it will
    use the same start node (`exploits`) as the `default_modules.json`
    file so that we can just use one node instead of multiple when parsing
    """
    start_dict = {"exploits": []}
    with open(path) as exploits:
        for exploit in exploits.readlines():
            # load everything into the dict
            start_dict["exploits"].append(exploit.strip())
    if filename is None:
        filename_path = "{}/etc/json/{}.json".format(os.getcwd(), random_file_name())
    else:
        filename_path = filename
    with open(filename_path, "a+") as exploits:
        # sort and indent to make it look pretty
        _data = json.dumps(start_dict, indent=4, sort_keys=True)
        exploits.write(_data)
    return filename_path
