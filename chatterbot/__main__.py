import sys


if __name__ == '__main__':
    import importlib

    if '--version' in sys.argv:
        chatterbot = importlib.import_module('chatterbot')
        print(chatterbot.__version__)

    if 'list_nltk_data' in sys.argv:
        import os
        import nltk.data

        data_directories = []

        # Find each data directory in the NLTK path that has content
        for path in nltk.data.path:
            if os.path.exists(path):
                if os.listdir(path):
                    data_directories.append(path)

        print(os.linesep.join(data_directories))
