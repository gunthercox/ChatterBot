from nltk.corpus import stopwords
from chatterbot.utils import nltk_download_corpus

class StopWordsManager(object):
    """
    A stop words utility class.
    """

    def __init__(self):
        # Download the stopwords data only if it is not already downloaded
        nltk_download_corpus('stopwords')

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
