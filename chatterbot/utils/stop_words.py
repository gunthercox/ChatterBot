from nltk.corpus import stopwords


class StopWordsManager():
    """
    A custom-implementation of Stop words. Not many
    features are supported at the moment, only:
    1) remove_stopwords: Removes the stopwords of the
        passed language from the tokens given
    2) words: Returns a list of stopwords for a given
        language
    """

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
