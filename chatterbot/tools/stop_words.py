class StopWordsManager(object):
    """
    A stop words utility class.
    """

    def remove_stopwords(self, language, tokens):
        """
        Takes a language (i.e. 'english'), and a set of word tokens.
        Returns the tokenized text with any stopwords removed.
        """
        from nltk.corpus import stopwords

        # Get the stopwords for the specified language
        stop_words = stopwords.words(language)

        # Remove the stop words from the set of word tokens
        tokens = set(tokens) - set(stop_words)

        return tokens
