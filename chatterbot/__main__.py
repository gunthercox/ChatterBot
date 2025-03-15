"""
Example usage for ChatterBot command line arguments:

python -m chatterbot --help
"""

import sys


def get_chatterbot_version():
    """
    Return the version of the current package.
    """
    from chatterbot import __version__

    return __version__


if __name__ == '__main__':
    if '--version' in sys.argv:
        print(get_chatterbot_version())
    elif '--help' in sys.argv:
        print('usage: chatterbot [--version, --help]')
        print('  --version: Print the version of ChatterBot')
        print('  --help: Print this help message')
        print()
        print('Documentation at https://docs.chatterbot.us')
