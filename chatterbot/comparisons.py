"""
This module contains various text-comparison algorithms
designed to compare one statement to another.
"""
from chatterbot.exceptions import OptionalDependencyImportError
from difflib import SequenceMatcher


class Comparator:

    def __init__(self, language):

        self.language = language

    def __call__(self, statement_a, statement_b):
        return self.compare(statement_a, statement_b)

    def compare(self, statement_a, statement_b):
        return 0


class LevenshteinDistance(Comparator):
    """
    Compare two statements based on the Levenshtein distance
    of each statement's text.

    For example, there is a 65% similarity between the statements
    "where is the post office?" and "looking for the post office"
    based on the Levenshtein distance algorithm.
    """

    def compare(self, statement_a, statement_b):
        """
        Compare the two input statements.

        :return: The percent of similarity between the text of the statements.
        :rtype: float
        """

        # Return 0 if either statement has a falsy text value
        if not statement_a.text or not statement_b.text:
            return 0

        # Get the lowercase version of both strings
        statement_a_text = str(statement_a.text.lower())
        statement_b_text = str(statement_b.text.lower())

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
    """

    def __init__(self, language):
        super().__init__(language)
        try:
            import spacy
        except ImportError:
            message = (
                'Unable to import "spacy".\n'
                'Please install "spacy" before using the SpacySimilarity comparator:\n'
                'pip3 install "spacy>=2.1,<2.2"'
            )
            raise OptionalDependencyImportError(message)

        self.nlp = spacy.load(self.language.ISO_639_1)

    def compare(self, statement_a, statement_b):
        """
        Compare the two input statements.

        :return: The percent of similarity between the closest synset distance.
        :rtype: float
        """
        document_a = self.nlp(statement_a.text)
        document_b = self.nlp(statement_b.text)

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
        try:
            import spacy
        except ImportError:
            message = (
                'Unable to import "spacy".\n'
                'Please install "spacy" before using the JaccardSimilarity comparator:\n'
                'pip3 install "spacy>=2.1,<2.2"'
            )
            raise OptionalDependencyImportError(message)

        self.nlp = spacy.load(self.language.ISO_639_1)

    def compare(self, statement_a, statement_b):
        """
        Return the calculated similarity of two
        statements based on the Jaccard index.
        """
        # Make both strings lowercase
        document_a = self.nlp(statement_a.text.lower())
        document_b = self.nlp(statement_b.text.lower())

        statement_a_lemmas = set([
            token.lemma_ for token in document_a if not token.is_stop
        ])
        statement_b_lemmas = set([
            token.lemma_ for token in document_b if not token.is_stop
        ])

        # Calculate Jaccard similarity
        numerator = len(statement_a_lemmas.intersection(statement_b_lemmas))
        denominator = float(len(statement_a_lemmas.union(statement_b_lemmas)))
        ratio = numerator / denominator

        return ratio
