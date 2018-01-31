"""
ChatterBot utility functions
"""


def import_module(dotted_path):
    """
    Imports the specified module based on the
    dot notated import path for the module.
    """
    import importlib

    module_parts = dotted_path.split('.')
    module_path = '.'.join(module_parts[:-1])
    module = importlib.import_module(module_path)

    return getattr(module, module_parts[-1])


def initialize_class(data, **kwargs):
    """
    :param data: A string or dictionary containing a import_path attribute.
    """
    if isinstance(data, dict):
        import_path = data.get('import_path')
        data.update(kwargs)
        Class = import_module(import_path)

        return Class(**data)
    else:
        Class = import_module(data)

        return Class(**kwargs)


def validate_adapter_class(validate_class, adapter_class):
    """
    Raises an exception if validate_class is not a
    subclass of adapter_class.

    :param validate_class: The class to be validated.
    :type validate_class: class

    :param adapter_class: The class type to check against.
    :type adapter_class: class

    :raises: Adapter.InvalidAdapterTypeException
    """
    from .adapters import Adapter

    # If a dictionary was passed in, check if it has an import_path attribute
    if isinstance(validate_class, dict):

        if 'import_path' not in validate_class:
            raise Adapter.InvalidAdapterTypeException(
                'The dictionary {} must contain a value for "import_path"'.format(
                    str(validate_class)
                )
            )

        # Set the class to the import path for the next check
        validate_class = validate_class.get('import_path')

    if not issubclass(import_module(validate_class), adapter_class):
        raise Adapter.InvalidAdapterTypeException(
            '{} must be a subclass of {}'.format(
                validate_class,
                adapter_class.__name__
            )
        )


def input_function():
    """
    Normalizes reading input between python 2 and 3.
    The function 'raw_input' becomes 'input' in Python 3.
    """
    import sys

    if sys.version_info[0] < 3:
        user_input = str(raw_input()) # NOQA

        # Avoid problems using format strings with unicode characters
        if user_input:
            user_input = user_input.decode('utf-8')

    else:
        user_input = input() # NOQA

    return user_input


def nltk_download_corpus(resource_path):
    """
    Download the specified NLTK corpus file
    unless it has already been downloaded.

    Returns True if the corpus needed to be downloaded.
    """
    from nltk.data import find
    from nltk import download
    from os.path import split, sep
    from zipfile import BadZipfile

    # Download the NLTK data only if it is not already downloaded
    _, corpus_name = split(resource_path)

    # From http://www.nltk.org/api/nltk.html
    # When using find() to locate a directory contained in a zipfile,
    # the resource name must end with the forward slash character.
    # Otherwise, find() will not locate the directory.
    #
    # Helps when resource_path=='sentiment/vader_lexicon''
    if not resource_path.endswith(sep):
        resource_path = resource_path + sep

    downloaded = False

    try:
        find(resource_path)
    except LookupError:
        download(corpus_name)
        downloaded = True
    except BadZipfile:
        raise BadZipfile(
            'The NLTK corpus file being opened is not a zipfile, '
            'or it has been corrupted and needs to be manually deleted.'
        )

    return downloaded


def remove_stopwords(tokens, language):
    """
    Takes a language (i.e. 'english'), and a set of word tokens.
    Returns the tokenized text with any stopwords removed.
    Stop words are words like "is, the, a, ..."

    Be sure to download the required NLTK corpus before calling this function:
    - from chatterbot.utils import nltk_download_corpus
    - nltk_download_corpus('corpora/stopwords')
    """
    from nltk.corpus import stopwords

    # Get the stopwords for the specified language
    stop_words = stopwords.words(language)

    # Remove the stop words from the set of word tokens
    tokens = set(tokens) - set(stop_words)

    return tokens


def get_response_time(chatbot):
    """
    Returns the amount of time taken for a given
    chat bot to return a response.

    :param chatbot: A chat bot instance.
    :type chatbot: ChatBot

    :returns: The response time in seconds.
    :rtype: float
    """
    import time

    start_time = time.time()

    chatbot.get_response('Hello')

    return time.time() - start_time


def print_progress_bar(description, iteration_counter, total_items, progress_bar_length=20):
    """
    Print progress bar
    :param description: Training description
    :type description: str

    :param iteration_counter: Incremental counter
    :type iteration_counter: int

    :param total_items: total number items
    :type total_items: int

    :param progress_bar_length: Progress bar length
    :type progress_bar_length: int

    :returns: void
    :rtype: void
    """
    import sys

    percent = float(iteration_counter) / total_items
    hashes = '#' * int(round(percent * progress_bar_length))
    spaces = ' ' * (progress_bar_length - len(hashes))
    sys.stdout.write("\r{0}: [{1}] {2}%".format(description, hashes + spaces, int(round(percent * 100))))
    sys.stdout.flush()
    if total_items == iteration_counter:
        print("\r")
