from nltk import word_tokenize


class POSTagger():
    """
    A custom-implementation of POS-taggers. Not many
    features are supported at the moment, only:
    1) tokenize: Returns the tokenized input text
    """

    def __init__(self):
        from nltk.data import find
        from nltk import download

        try:
            find('punkt.zip')
        except LookupError:
            download('punkt')

    def tokenize(self, text):
        """
        Takes an input string and tokenizes that text.
        Returns an array of tuples which contain
        the tokenized text.
        """

        return word_tokenize(text)
