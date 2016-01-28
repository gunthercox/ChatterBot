from nltk.corpus import wordnet


class Wordnet():
    """
    A custom-implementation of Wordnet. Not many
    features are supported at the moment, only:
    1) synsets: Returns the synsets of a token
    """

    def __init__(self):
        from nltk.data import find
        from nltk import download

        try:
            find('wordnet.zip')
        except LookupError:
            download('wordnet')

    def synsets(self, token):
        """
        Takes a token and returns the synsets for
        it.
        """
        return wordnet.synsets(token)
