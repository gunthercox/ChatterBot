from nltk.corpus import wordnet
from chatterbot.utils import nltk_download_corpus


class Wordnet(object):
    """
    A custom-implementation of Wordnet. Not many
    features are supported at the moment, only:
    1) synsets: Returns the synsets of a token
    """

    def __init__(self):
        # Download the wordnet data only if it is not already downloaded
        nltk_download_corpus('wordnet')

    def synsets(self, token):
        """
        Takes a token and returns the synsets for it.
        """
        return wordnet.synsets(token)
