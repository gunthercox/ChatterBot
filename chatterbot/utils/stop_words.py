from nltk.corpus import stopwords


class NLTKStopWordsManager():
    def __init__(self):
        from nltk.data import find
        from nltk import download

        try:
            find('stopwords.zip')
        except LookupError:
            download('stopwords')

    def remove_stopwords(self, language, tokens):
        """
        Takes a set of tokens and stopwords language
        and returns the tokenized text minus the
        stopwords.
        """
        stop_words = self.words(language)
        tokens = set(tokens) - set(excluded_words)

        return tokens

    def words(self, language):
        """
        Returns the stopwords for the given language.
        """

        return stopwords.words(language)
