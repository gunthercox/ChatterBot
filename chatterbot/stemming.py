import string
import nltk


class SimpleStemmer(object):
    """
    A very simple stemming algorithm that removes stopwords and punctuation.
    It then removes the beginning and ending characters of each word.
    This should work for any language.
    """

    def __init__(self, language='english'):
        from chatterbot.utils import nltk_download_corpus

        self.punctuation_table = str.maketrans(dict.fromkeys(string.punctuation))

        # Download the stopwords corpus if needed
        nltk_download_corpus('stopwords')

        # Get list of stopwords from the NLTK corpus
        self.stopwords = nltk.corpus.stopwords.words(language)
        self.stopwords.append('')

    def get_stemmed_word_list(self, text):

        # Remove punctuation
        text = text.translate(self.punctuation_table)

        # Make the text lowercase
        text = text.lower()

        words = []

        # Generate the stemmed text
        for word in text.split(' '):

            # Remove stopwords
            if word not in self.stopwords:

                # Chop off the ends of the word
                start = len(word) // 4
                stop = start * -1
                word = word[start:stop]

                if word:
                    words.append(word)

        return words

    def get_bigram_pair_string(self, text):
        """
        Return bigram pairs of stemmed text for a given string.
        For example:

        "Hello Dr. Salazar. How are you today?"
        "[ell alaza] [alaza oda]"
        "ellalaza alazaoda"
        """
        words = self.get_stemmed_word_list(text)

        bigrams = []

        word_count = len(words)

        if word_count <= 1:
            bigrams = words

        for index in range(0, word_count - 1):
            bigram = words[index] + words[index + 1]
            bigrams.append(bigram)

        return ' '.join(bigrams)

    def stem(self, text):
        words = self.get_stemmed_word_list(text)

        return ' '.join(words)
