import sys


def get_chatterbot_version():
    from chatterbot import __version__

    return __version__


if __name__ == '__main__':
    if '--version' in sys.argv:
        print(get_chatterbot_version())
