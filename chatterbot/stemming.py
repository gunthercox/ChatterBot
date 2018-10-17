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

        # Get list of stopwords from the NLTK corpus
        self.stopwords = nltk.corpus.stopwords.words(language)
        self.stopwords.append('')

    def stem(self, text):

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

                words.append(word)

        return ' '.join(words)[:-1]
