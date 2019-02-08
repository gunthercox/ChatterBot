from .comparator import Comparator
from chatterbot import utils
from chatterbot import languages
from nltk.corpus import wordnet, stopwords
from nltk import word_tokenize
import itertools


class SynsetDistance(Comparator):
    """
    Calculate the similarity of two statements.
    This is based on the total maximum synset similarity between each word in each sentence.

    This algorithm uses the `wordnet`_ functionality of `NLTK`_ to determine the similarity
    of two statements based on the path similarity between each token of each statement.
    This is essentially an evaluation of the closeness of synonyms.
    """

    def __init__(self):
        super().__init__()

        self.language = languages.ENG

        self.stopwords = None

    def initialize_nltk_wordnet(self):
        """
        Download required NLTK corpora if they have not already been downloaded.
        """
        utils.nltk_download_corpus('corpora/wordnet')

    def initialize_nltk_punkt(self):
        """
        Download required NLTK corpora if they have not already been downloaded.
        """
        utils.nltk_download_corpus('tokenizers/punkt')

    def initialize_nltk_stopwords(self):
        """
        Download required NLTK corpora if they have not already been downloaded.
        """
        utils.nltk_download_corpus('corpora/stopwords')

    def get_stopwords(self):
        """
        Get the list of stopwords from the NLTK corpus.
        """
        if self.stopwords is None:
            self.stopwords = stopwords.words(self.language.ENGLISH_NAME.lower())

        return self.stopwords

    def compare(self, statement, other_statement):
        """
        Compare the two input statements.

        :return: The percent of similarity between the closest synset distance.
        :rtype: float

        .. _wordnet: http://www.nltk.org/howto/wordnet.html
        .. _NLTK: http://www.nltk.org/
        """
        tokens1 = word_tokenize(statement.text.lower())
        tokens2 = word_tokenize(other_statement.text.lower())

        # Get the stopwords for the current language
        stop_word_set = set(self.get_stopwords())

        # Remove all stop words from the list of word tokens
        tokens1 = set(tokens1) - stop_word_set
        tokens2 = set(tokens2) - stop_word_set

        # The maximum possible similarity is an exact match
        # Because path_similarity returns a value between 0 and 1,
        # max_possible_similarity is the number of words in the longer
        # of the two input statements.
        max_possible_similarity = min(
            len(tokens1),
            len(tokens2)
        ) / max(
            len(tokens1),
            len(tokens2)
        )

        max_similarity = 0.0

        # Get the highest matching value for each possible combination of words
        for combination in itertools.product(*[tokens1, tokens2]):

            synset1 = wordnet.synsets(combination[0])
            synset2 = wordnet.synsets(combination[1])

            if synset1 and synset2:

                # Get the highest similarity for each combination of synsets
                for synset in itertools.product(*[synset1, synset2]):
                    similarity = synset[0].path_similarity(synset[1])

                    if similarity and (similarity > max_similarity):
                        max_similarity = similarity

        if max_possible_similarity == 0:
            return 0

        return max_similarity / max_possible_similarity
