import sys


if __name__ == '__main__':
    import chatterbot

    if '--version' in sys.argv:
        print(chatterbot.__version__)

    if 'list_nltk_data' in sys.argv:
        import nltk.data

        print('\n'.join(nltk.data.path))
