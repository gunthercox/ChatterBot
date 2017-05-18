import sys


if __name__ == '__main__':
    from . import chatterbot

    if '--version' in sys.argv:
        print((chatterbot.__version__))
