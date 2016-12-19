"""
ChatterBot utility functions
"""


def clean_whitespace(text):
    """
    Remove any extra whitespace and line breaks as needed.
    """
    import re

    # Replace linebreaks with spaces
    text = text.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')

    # Remove any leeding or trailing whitespace
    text = text.strip()

    # Remove consecutive spaces
    text = re.sub(' +', ' ', text)

    return text


def clean(text):
    """
    A function for cleaning a string of text.
    Returns valid ASCII characters.
    """
    import unicodedata
    import sys

    text = clean_whitespace(text)

    # Remove links from message
    # text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)

    # Replace HTML escape characters
    if sys.version_info[0] < 3:
        from HTMLParser import HTMLParser
        parser = HTMLParser()
        text = parser.unescape(text)
    else:
        import html
        text = html.unescape(text)

    # Normalize unicode characters
    # 'raw_input' is just 'input' in python3
    if sys.version_info[0] < 3:
        text = unicode(text)
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')

    return str(text)


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
        import_path = data.pop('import_path')
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
        origional_data = validate_class.copy()
        validate_class = validate_class.get('import_path')

        if not validate_class:
            raise Adapter.InvalidAdapterTypeException(
                'The dictionary {} must contain a value for "import_path"'.format(
                    str(origional_data)
                )
            )

    if not issubclass(import_module(validate_class), Adapter):
        raise Adapter.InvalidAdapterTypeException(
            '{} must be a subclass of {}'.format(
                validate_class,
                Adapter.__name__
            )
        )

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
        user_input = str(raw_input())

        # Avoid problems using format strings with unicode characters
        if user_input:
            user_input = user_input.decode('utf-8')

    else:
        user_input = input()

    return user_input


def nltk_download_corpus(corpus_name):
    """
    Download the specified NLTK corpus file
    unless it has already been downloaded.

    Returns True if the corpus needed to be downloaded.
    """
    from nltk.data import find
    from nltk import download

    # Download the wordnet data only if it is not already downloaded
    zip_file = '{}.zip'.format(corpus_name)
    downloaded = False

    try:
        find(zip_file)
    except LookupError:
        download(corpus_name)
        downloaded = True

    return downloaded


def remove_stopwords(tokens, language):
    """
    Takes a language (i.e. 'english'), and a set of word tokens.
    Returns the tokenized text with any stopwords removed.
    Stop words are words like "is, the, a, ..."
    """
    from nltk.corpus import stopwords

    # Get the stopwords for the specified language
    stop_words = stopwords.words(language)

    # Remove the stop words from the set of word tokens
    tokens = set(tokens) - set(stop_words)

    return tokens
