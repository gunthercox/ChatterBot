import string
import nltk


class SimpleStemmer(object):
    """
    A very simple stemming algorithm that removes stopwords and punctuation.
    It then removes the beginning and ending characters of each word.
    This should work for any language.
    """

    def __init__(self, language='english'):
        self.punctuation_table = str.maketrans(dict.fromkeys(string.punctuation))

        self.language = language

        self.stopwords = None

    def get_stopwords(self):
        """
        Get the list of stopwords from the NLTK corpus.
        """
        if not self.stopwords:
            self.stopwords = nltk.corpus.stopwords.words(self.language)

        return self.stopwords

    def get_initialization_functions(self):
        """
        Return all initialization methods for the comparison algorithm.
        Initialization methods must start with 'initialize_' and
        take no parameters.
        """
        initialization_methods = [
            (
                method,
                getattr(self, method),
            ) for method in dir(self) if method.startswith('initialize_')
        ]

        return {
            key: value for (key, value) in initialization_methods
        }

    def initialize(self):
        for function in self.get_initialization_functions().values():
            function()

    def initialize_nltk_stopwords(self):
        """
        Download required NLTK stopwords corpus if it has not already been downloaded.
        """
        from chatterbot.utils import nltk_download_corpus

        nltk_download_corpus('stopwords')

    def get_stemmed_words(self, text, size=4):

        stemmed_words = []

        # Make the text lowercase
        text = text.lower()

        # Remove punctuation
        text_with_punctuation_removed = text.translate(self.punctuation_table)

        if text_with_punctuation_removed:
            text = text_with_punctuation_removed

        words = text.split(' ')

        # Do not stem singe-word strings that are less than the size limit for characters
        if len(words) == 1 and len(words[0]) < size:
            return words

        # Generate the stemmed text
        for word in words:

            # Remove stopwords
            if word not in self.get_stopwords():

                # Chop off the ends of the word
                start = len(word) // size
                stop = start * -1
                word = word[start:stop]

                if word:
                    stemmed_words.append(word)

        # Return the word list if it could not be stemmed
        if not stemmed_words and words:
            return words

        return stemmed_words

    def get_bigram_pair_string(self, text):
        """
        Return bigram pairs of stemmed text for a given string.
        For example:

        "Hello Dr. Salazar. How are you today?"
        "[ell alaza] [alaza oda]"
        "ellalaza alazaoda"
        """
        words = self.get_stemmed_words(text)

        bigrams = []

        word_count = len(words)

        if word_count <= 1:
            bigrams = words

        for index in range(0, word_count - 1):
            bigram = words[index] + words[index + 1]
            bigrams.append(bigram)

        return ' '.join(bigrams)
