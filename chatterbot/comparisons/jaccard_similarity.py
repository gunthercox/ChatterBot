
from .comparator import Comparator
from chatterbot import utils
from chatterbot import languages
from nltk.corpus import stopwords
from nltk import pos_tag, tokenize
import string


class JaccardSimilarity(Comparator):
    """
    Calculates the similarity of two statements based on the Jaccard index.

    The Jaccard index is composed of a numerator and denominator.
    In the numerator, we count the number of items that are shared between the sets.
    In the denominator, we count the total number of items across both sets.
    Let's say we define sentences to be equivalent if 50% or more of their tokens are equivalent.
    Here are two sample sentences:

        The young cat is hungry.
        The cat is very hungry.

    When we parse these sentences to remove stopwords, we end up with the following two sets:

        {young, cat, hungry}
        {cat, very, hungry}

    In our example above, our intersection is {cat, hungry}, which has count of two.
    The union of the sets is {young, cat, very, hungry}, which has a count of four.
    Therefore, our `Jaccard similarity index`_ is two divided by four, or 50%.
    Given our similarity threshold above, we would consider this to be a match.

    .. _`Jaccard similarity index`: https://en.wikipedia.org/wiki/Jaccard_index
    """

    def __init__(self):
        super().__init__()

        self.punctuation_table = str.maketrans(dict.fromkeys(string.punctuation))

        self.language = languages.ENG

        self.stopwords = None

        self.lemmatizer = None

    def initialize_nltk_wordnet(self):
        """
        Download the NLTK wordnet corpora that is required for this algorithm
        to run only if the corpora has not already been downloaded.
        """
        utils.nltk_download_corpus('corpora/wordnet')

    def initialize_nltk_averaged_perceptron_tagger(self):
        """
        Download the NLTK averaged perceptron tagger that is required for this algorithm
        to run only if the corpora has not already been downloaded.
        """
        utils.nltk_download_corpus('averaged_perceptron_tagger')

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

    def get_lemmatizer(self):
        """
        Get the lemmatizer.
        """
        if self.lemmatizer is None:
            from nltk.stem.wordnet import WordNetLemmatizer

            self.lemmatizer = WordNetLemmatizer()

        return self.lemmatizer

    def compare(self, statement, other_statement):
        """
        Return the calculated similarity of two
        statements based on the Jaccard index.
        """
        # Get the stopwords for the current language
        stopwords = self.get_stopwords()

        lemmatizer = self.get_lemmatizer()

        # Make both strings lowercase
        a = statement.text.lower()
        b = other_statement.text.lower()

        # Remove punctuation from each string
        a = a.translate(self.punctuation_table)
        b = b.translate(self.punctuation_table)

        pos_a = pos_tag(tokenize.word_tokenize(a))
        pos_b = pos_tag(tokenize.word_tokenize(b))

        lemma_a = [
            lemmatizer.lemmatize(
                token, utils.treebank_to_wordnet(pos)
            ) for token, pos in pos_a if token not in stopwords
        ]
        lemma_b = [
            lemmatizer.lemmatize(
                token, utils.treebank_to_wordnet(pos)
            ) for token, pos in pos_b if token not in stopwords
        ]

        # Calculate Jaccard similarity
        numerator = len(set(lemma_a).intersection(lemma_b))
        denominator = float(len(set(lemma_a).union(lemma_b)))
        ratio = numerator / denominator

        return ratio
