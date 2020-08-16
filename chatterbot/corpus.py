import os
import io
import glob
import yaml
from chatterbot_corpus.corpus import DATA_DIRECTORY


CORPUS_EXTENSION = 'yml'


def get_file_path(dotted_path, extension='json'):
    """
    Reads a dotted file path and returns the file path.
    """
    # If the operating system's file path seperator character is in the string
    if os.sep in dotted_path or '/' in dotted_path:
        # Assume the path is a valid file path
        return dotted_path

    parts = dotted_path.split('.')
    if parts[0] == 'chatterbot':
        parts.pop(0)
        parts[0] = DATA_DIRECTORY

    corpus_path = os.path.join(*parts)

    path_with_extension = '{}.{}'.format(corpus_path, extension)
    if os.path.exists(path_with_extension):
        corpus_path = path_with_extension

    return corpus_path


def read_corpus(file_name):
    """
    Read and return the data from a corpus json file.
    """
    with io.open(file_name, encoding='utf-8') as data_file:
        return yaml.load(data_file)


def list_corpus_files(dotted_path):
    """
    Return a list of file paths to each data file in the specified corpus.
    """
    corpus_path = get_file_path(dotted_path, extension=CORPUS_EXTENSION)
    paths = []

    if os.path.isdir(corpus_path):
        paths = glob.glob(corpus_path + '/**/*.' + CORPUS_EXTENSION, recursive=True)
    else:
        paths.append(corpus_path)

    paths.sort()
    return paths


def load_corpus(*data_file_paths):
    """
    Return the data contained within a specified corpus.
    """
    for file_path in data_file_paths:
        corpus = []
        corpus_data = read_corpus(file_path)

        conversations = corpus_data.get('conversations', [])
        corpus.extend(conversations)

        categories = corpus_data.get('categories', [])

        yield corpus, categories, file_path
