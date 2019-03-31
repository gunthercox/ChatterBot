import importlib
import sys


def get_chatterbot_version():
    chatterbot = importlib.import_module('chatterbot')
    return chatterbot.__version__


if __name__ == '__main__':
    if '--version' in sys.argv:
        print(get_chatterbot_version())
