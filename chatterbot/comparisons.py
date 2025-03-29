"""
This module contains various text-comparison algorithms
designed to compare one statement to another.
"""
from chatterbot.utils import get_model_for_language
from difflib import SequenceMatcher
import spacy


class Comparator:
    """
    Base class establishing the interface that all comparators should implement.
    """

    def __init__(self, language):

        self.language = language

    def __call__(self, statement_a, statement_b):
        return self.compare(statement_a, statement_b)

    def compare_text(self, text_a: str, text_b: str) -> float:
        """
        Implemented in subclasses: compare text_a to text_b.

        :return: The percent of similarity between the statements based on the implemented algorithm.
        """
        return 0

    def compare(self, statement_a, statement_b) -> float:
        """
        :return: The percent of similarity between the statements based on the implemented algorithm.
        """
        return self.compare_text(statement_a.text, statement_b.text)


class LevenshteinDistance(Comparator):
    """
    Compare two statements based on the Levenshtein distance
    of each statement's text.

    For example, there is a 65% similarity between the statements
    "where is the post office?" and "looking for the post office"
    based on the Levenshtein distance algorithm.
    """

    def compare_text(self, text_a: str, text_b: str) -> float:
        """
        Compare the two pieces of text.

        :return: The percent of similarity between the text of the statements.
        """

        # Return 0 if either statement has a None text value
        if text_a is None or text_b is None:
            return 0

        # Get the lowercase version of both strings
        statement_a_text = str(text_a.lower())
        statement_b_text = str(text_b.lower())

        similarity = SequenceMatcher(
            None,
            statement_a_text,
            statement_b_text
        )

        # Calculate a decimal percent of the similarity
        percent = round(similarity.ratio(), 2)

        return percent


class SpacySimilarity(Comparator):
    """
    Calculate the similarity of two statements using Spacy models.

    NOTE:
        You will also need to download a ``spacy`` model to use for tagging. Internally these are used to determine parts of speech for words.

        The easiest way to do this is to use the ``spacy download`` command directly:

        .. code-block:: python

           python -m spacy download en_core_web_sm
           python -m spacy download de_core_news_sm

        Alternatively, the ``spacy`` models can be installed as Python packages. The following lines could be included in a ``requirements.txt`` or ``pyproject.yml`` file if you needed to pin specific versions:

        .. code-block:: text

           https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-2.3.0/en_core_web_sm-2.3.0.tar.gz#egg=en_core_web_sm
           https://github.com/explosion/spacy-models/releases/download/de_core_news_sm-2.3.0/de_core_news_sm-2.3.0.tar.gz#egg=de_core_news_sm

    """

    def __init__(self, language):
        super().__init__(language)

        model = get_model_for_language(language)

        # Disable the Named Entity Recognition (NER) component because it is not necessary
        self.nlp = spacy.load(model, exclude=['ner'])

    def compare_text(self, text_a: str, text_b: str) -> float:
        """
        Compare the similarity of two strings.

        :return: The percent of similarity between the closest synset distance.
        """

        # Return 0 if either statement has a None text value
        if text_a is None or text_b is None:
            return 0

        document_a = self.nlp(text_a)
        document_b = self.nlp(text_b)

        return document_a.similarity(document_b)


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

    def __init__(self, language):
        super().__init__(language)

        model = get_model_for_language(language)

        # Disable the Named Entity Recognition (NER) component because it is not necessary
        self.nlp = spacy.load(model, exclude=['ner'])

    def compare_text(self, text_a: str, text_b: str) -> float:
        """
        Return the calculated similarity of two
        statements based on the Jaccard index.
        """

        # Return 0 if either statement has a None text value
        if text_a is None or text_b is None:
            return 0

        # Make both strings lowercase
        document_a = self.nlp(text_a.lower())
        document_b = self.nlp(text_b.lower())

        statement_a_lemmas = frozenset([
            token.lemma_ for token in document_a if not token.is_stop
        ])
        statement_b_lemmas = frozenset([
            token.lemma_ for token in document_b if not token.is_stop
        ])

        # Calculate Jaccard similarity
        numerator = len(statement_a_lemmas.intersection(statement_b_lemmas))
        denominator = float(len(statement_a_lemmas.union(statement_b_lemmas)))
        ratio = numerator / denominator

        return ratio
