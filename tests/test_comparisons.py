"""
Test ChatterBot's statement comparison algorithms.
"""

from unittest import TestCase
from chatterbot.conversation import Statement
from chatterbot import comparisons


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


class SpacySimilarityTests(TestCase):

    def test_exact_match_different_stopwords(self):
        """
        Test sentences with different stopwords.
        """
        statement = Statement(text='What is matter?')
        other_statement = Statement(text='What is the matter?')

        value = comparisons.spacy_similarity(statement, other_statement)

        self.assertAlmostEqual(value, 0.9, places=1)

    def test_exact_match_different_capitalization(self):
        """
        Test that text capitalization is ignored.
        """
        statement = Statement(text='Hi HoW ArE yOu?')
        other_statement = Statement(text='hI hOw are YoU?')

        value = comparisons.spacy_similarity(statement, other_statement)

        self.assertAlmostEqual(value, 0.8, places=1)


class JaccardSimilarityTestCase(TestCase):

    def test_exact_match_different_capitalization(self):
        """
        Test that text capitalization is ignored.
        """
        statement = Statement(text='Hi HoW ArE yOu?')
        other_statement = Statement(text='hI hOw are YoU?')

        value = comparisons.jaccard_similarity(statement, other_statement)

        self.assertEqual(value, 1)
