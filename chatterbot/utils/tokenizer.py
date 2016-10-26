class Tokenizer(object):
    """
    A string tokenizaton utility class.
    """

    def __init__(self):
        from nltk.data import find
        from nltk import download

        # Download the punkt data only if it is not already downloaded
        try:
            find('punkt.zip')
        except LookupError:
            download('punkt')

    def get_tokens(self, text, language='english', exclude_stop_words=True):
        """
        Takes a string and converts it to a tuple of each word.
        Skips common stop words such as ("is, the, a, ...")
        if 'exclude_stop_words' is True.
        """
        from chatterbot.utils.stop_words import StopWordsManager
        from nltk import word_tokenize

        stopwords = StopWordsManager()
        tokens = word_tokenize(text.lower())

        # Remove all stop words from the list of word tokens
        if exclude_stop_words:
            tokens = stopwords.remove_stopwords(language, tokens)

        return tokens