import string
from nltk import pos_tag
from nltk.corpus import wordnet, stopwords


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

    def initialize_nltk_stopwords(self):
        """
        Download required NLTK stopwords corpus if it has not already been downloaded.
        """
        from chatterbot.utils import nltk_download_corpus

        nltk_download_corpus('stopwords')

    def get_stopwords(self):
        """
        Get the list of stopwords from the NLTK corpus.
        """
        if not self.stopwords:
            self.stopwords = stopwords.words(self.language)

        return self.stopwords

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


def treebank_to_wordnet(pos):
    """
    * https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html
    * http://www.nltk.org/_modules/nltk/corpus/reader/wordnet.html
    """
    data_map = {
        'N': wordnet.NOUN,
        'J': wordnet.ADJ,
        'V': wordnet.VERB,
        'R': wordnet.ADV
    }

    return data_map.get(pos[0])


class PosHypernymStemmer(object):
    """
    For each non-stopword in a string, return a string where each word is a
    hypernym preceded by the part of speech of the word before it.
    """

    def __init__(self, language='english'):
        self.punctuation_table = str.maketrans(dict.fromkeys(string.punctuation))

        self.language = language

        self.stopwords = None

    def initialize_nltk_stopwords(self):
        """
        Download required NLTK stopwords corpus if it has not already been downloaded.
        """
        from chatterbot.utils import nltk_download_corpus

        nltk_download_corpus('stopwords')

    def initialize_nltk_wordnet(self):
        """
        Download required NLTK corpora if they have not already been downloaded.
        """
        from chatterbot.utils import nltk_download_corpus

        nltk_download_corpus('corpora/wordnet')

    def get_stopwords(self):
        """
        Get the list of stopwords from the NLTK corpus.
        """
        if not self.stopwords:
            self.stopwords = stopwords.words(self.language)

        return self.stopwords

    def get_hypernyms(self, pos_tags):
        """
        Return the hypernyms for each word in a list of POS tagged words.
        """
        results = []

        for word, pos in pos_tags:
            synsets = wordnet.synsets(word, treebank_to_wordnet(pos))

            if synsets:
                synset = synsets[0]
                hypernyms = synset.hypernyms()

                if hypernyms:
                    results.append(hypernyms[0].name().split('.')[0])
                else:
                    results.append(word)
            else:
                results.append(word)

        return results

    def get_bigram_pair_string(self, text):
        """
        For example:
        What a beautiful swamp

        becomes:

        DT:beautiful JJ:wetland
        """
        words = text.split()

        # Separate punctuation from last word in string
        if words:
            word_with_punctuation_removed = words[-1].strip(string.punctuation)

            if word_with_punctuation_removed:
                words[-1] = word_with_punctuation_removed

        pos_tags = pos_tag(words)

        hypernyms = self.get_hypernyms(pos_tags)

        high_quality_bigrams = []
        all_bigrams = []

        word_count = len(words)

        if word_count <= 1:
            all_bigrams = words
            if all_bigrams:
                all_bigrams[0] = all_bigrams[0].lower()

        for index in range(1, word_count):
            word = words[index].lower()
            previous_word_pos = pos_tags[index][1]
            if word not in self.get_stopwords() and len(word) > 1:
                bigram = previous_word_pos + ':' + hypernyms[index].lower()
                high_quality_bigrams.append(bigram)
                all_bigrams.append(bigram)
            else:
                bigram = previous_word_pos + ':' + word
                all_bigrams.append(bigram)

        if high_quality_bigrams:
            all_bigrams = high_quality_bigrams

        return ' '.join(all_bigrams)
