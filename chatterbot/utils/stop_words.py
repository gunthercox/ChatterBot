from nltk.corpus import stopwords


class StopWordsManager(object):
    """
    A stop words utility class.
    1) remove_stopwords: Removes the stopwords of the
        passed language from the tokens given
    """

    def __init__(self):
        from nltk.data import find
        from nltk import download
        import os

        # Download the stopwords data only if it is not already downloaded
        stopwords_path = None
        if os.name == 'nt':
            stopwords_path = os.path.join(os.getenv('APPDATA'), 'nltk_data',
                                                'corpora', 'stopwords.zip')
        else:
            stopwords_path = os.path.join(os.path.expanduser('~'), 'nltk_data',
                                                'corpora', 'stopwords.zip')
        try:
            if not os.path.isfile(stopwords_path):
                find('stopwords.zip')
        except LookupError:
            download('stopwords')

    def remove_stopwords(self, language, tokens):
        """
        Takes a language (i.e. 'english'), and a set of word tokens.
        Returns the tokenized text with any stopwords removed.
        """
        # Get the stopwords for the specified language
        stop_words = stopwords.words(language)

        # Remove the stop words from the set of word tokens
        tokens = set(tokens) - set(stop_words)

        return tokens