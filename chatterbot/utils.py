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
    import os

    # Download the wordnet data only if it is not already downloaded
    zip_file = '{}.zip'.format(corpus_name)
    downloaded = False
    wordnet_path = None
    if os.name == 'nt':
        wordnet_path = os.path.join(
            os.getenv('APPDATA'), 'nltk_data', 'corpora', zip_file
        )
    else:
        wordnet_path = os.path.join(
            os.path.expanduser('~'), 'nltk_data', 'corpora', zip_file
        )

    try:
        if not os.path.isfile(wordnet_path):
            find(zip_file)
    except LookupError:
        download('wordnet')
        downloaded = True

    return downloaded
