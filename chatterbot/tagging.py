import string
from chatterbot.utils import treebank_to_wordnet
from nltk import pos_tag
from nltk.data import load as load_data
from nltk.corpus import wordnet, stopwords


class PosHypernymTagger(object):
    """
    For each non-stopword in a string, return a string where each word is a
    hypernym preceded by the part of speech of the word before it.
    """

    def __init__(self, language='english'):
        self.sentence_detector = load_data('tokenizers/punkt/english.pickle')

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
        WORD_INDEX = 0
        POS_INDEX = 1

        pos_tags = []

        for sentence in self.sentence_detector.tokenize(text.strip()):

            # Remove punctuation
            if sentence and sentence[-1] in string.punctuation:
                sentence_with_punctuation_removed = sentence[:-1]

                if sentence_with_punctuation_removed:
                    sentence = sentence_with_punctuation_removed

            words = sentence.split()

            pos_tags.extend(pos_tag(words))

        hypernyms = self.get_hypernyms(pos_tags)

        high_quality_bigrams = []
        all_bigrams = []

        word_count = len(pos_tags)

        if word_count == 1:
            all_bigrams.append(
                pos_tags[0][WORD_INDEX].lower()
            )

        for index in range(1, word_count):
            word = pos_tags[index][WORD_INDEX].lower()
            previous_word_pos = pos_tags[index - 1][POS_INDEX]
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
