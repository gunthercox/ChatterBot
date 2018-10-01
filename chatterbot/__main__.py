import importlib
import sys
import os


def get_chatterbot_version():
    chatterbot = importlib.import_module('chatterbot')
    return chatterbot.__version__


def get_nltk_data_directories():
    import nltk.data

    data_directories = []

    # Find each data directory in the NLTK path that has content
    for path in nltk.data.path:
        if os.path.exists(path):
            if os.listdir(path):
                data_directories.append(path)

    return os.linesep.join(data_directories)


if __name__ == '__main__':
    if '--version' in sys.argv:
        print(get_chatterbot_version())

    if 'list_nltk_data' in sys.argv:
        print(get_nltk_data_directories())
