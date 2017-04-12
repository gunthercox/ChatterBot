import sys


if __name__ == '__main__':
    import chatterbot

    if '--version' in sys.argv:
        print(chatterbot.__version__)