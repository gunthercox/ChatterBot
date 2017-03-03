"""
Test ChatterBot's statement comparison algorithms.
"""

from unittest import TestCase, SkipTest
from chatterbot.conversation import Statement
from chatterbot import comparisons


class LevenshteinDistanceTestCase(TestCase):

    def test_levenshtein_distance_statement_false(self):
        """
        Falsy values should match by zero.
        """
        statement = Statement('')
        other_statement = Statement('Hello')

        value = comparisons.levenshtein_distance(statement, other_statement)

        self.assertEqual(value, 0)

    def test_levenshtein_distance_other_statement_false(self):
        """
        Falsy values should match by zero.
        """
        statement = Statement('Hello')
        other_statement = Statement('')

        value = comparisons.levenshtein_distance(statement, other_statement)

        self.assertEqual(value, 0)

    def test_exact_match_different_capitalization(self):
        """
        Test that text capitalization is ignored.
        """
        statement = Statement('Hi HoW ArE yOu?')
        other_statement = Statement('hI hOw are YoU?')

        value = comparisons.levenshtein_distance(statement, other_statement)

        self.assertEqual(value, 1)


class SynsetDistanceTestCase(TestCase):

    def test_exact_match_different_capitalization(self):
        """
        Test that text capitalization is ignored.
        """
        raise SkipTest('This test needs to be created.')


class SentimentComparisonTestCase(TestCase):

    def test_exact_match_different_capitalization(self):
        """
        Test that text capitalization is ignored.
        """
        statement = Statement('Hi HoW ArE yOu?')
        other_statement = Statement('hI hOw are YoU?')

        value = comparisons.sentiment_comparison(statement, other_statement)

        self.assertEqual(value, 1)


class JaccardSimilarityTestCase(TestCase):

    def test_exact_match_different_capitalization(self):
        """
        Test that text capitalization is ignored.
        """
        raise SkipTest('This test needs to be created.')

