from nltk import word_tokenize
from nltk import pos_tag


class POSTagger():

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

    def tag(self, tokens):
        """
        Takes a set of tokens and returns the tagged tokens.
        """

        return pos_tag(tokens)
