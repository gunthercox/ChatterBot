from nltk.corpus import wordnet


class NLTKWordnet():
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
