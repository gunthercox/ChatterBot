"""
Test ChatterBot's statement comparison algorithms.
"""

from unittest import TestCase
from chatterbot.conversation import Statement
from chatterbot import comparisons
from chatterbot import utils


class LevenshteinDistanceTestCase(TestCase):

    def test_levenshtein_distance_statement_false(self):
        """
        Falsy values should match by zero.
        """
        statement = Statement(text='')
        other_statement = Statement(text='Hello')

        value = comparisons.levenshtein_distance(statement, other_statement)

        self.assertEqual(value, 0)

    def test_levenshtein_distance_other_statement_false(self):
        """
        Falsy values should match by zero.
        """
        statement = Statement(text='Hello')
        other_statement = Statement(text='')

        value = comparisons.levenshtein_distance(statement, other_statement)

        self.assertEqual(value, 0)

    def test_levenshtein_distance_statement_integer(self):
        """
        Test that an exception is not raised if a statement is initialized
        with an integer value as its text attribute.
        """
        statement = Statement(text=2)
        other_statement = Statement(text='Hello')

        value = comparisons.levenshtein_distance(statement, other_statement)

        self.assertEqual(value, 0)

    def test_exact_match_different_capitalization(self):
        """
        Test that text capitalization is ignored.
        """
        statement = Statement(text='Hi HoW ArE yOu?')
        other_statement = Statement(text='hI hOw are YoU?')

        value = comparisons.levenshtein_distance(statement, other_statement)

        self.assertEqual(value, 1)


class SynsetDistanceTestCase(TestCase):

    def test_exact_match_different_stopwords(self):
        """
        Test that stopwords are ignored.
        """
        statement = Statement(text='What is matter?')
        other_statement = Statement(text='What is the matter?')

        value = comparisons.synset_distance(statement, other_statement)

        self.assertEqual(value, 1)

    def test_exact_match_different_capitalization(self):
        """
        Test that text capitalization is ignored.
        """
        statement = Statement(text='Hi HoW ArE yOu?')
        other_statement = Statement(text='hI hOw are YoU?')

        value = comparisons.synset_distance(statement, other_statement)

        self.assertEqual(value, 1)


class SentimentComparisonTestCase(TestCase):

    def setUp(self):
        super().setUp()

        # Make sure the required NLTK data files are downloaded
        for function in utils.get_initialization_functions(
            comparisons, 'sentiment_comparison'
        ).values():
            function()

    def test_exact_match_different_capitalization(self):
        """
        Test that text capitalization is ignored.
        """
        statement = Statement(text='Hi HoW ArE yOu?')
        other_statement = Statement(text='hI hOw are YoU?')

        value = comparisons.sentiment_comparison(statement, other_statement)

        self.assertEqual(value, 1)


class JaccardSimilarityTestCase(TestCase):

    def test_exact_match_different_capitalization(self):
        """
        Test that text capitalization is ignored.
        """
        statement = Statement(text='Hi HoW ArE yOu?')
        other_statement = Statement(text='hI hOw are YoU?')

        value = comparisons.jaccard_similarity(statement, other_statement)

        self.assertEqual(value, 1)
