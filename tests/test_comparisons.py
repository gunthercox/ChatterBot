"""
Test ChatterBot's statement comparison algorithms.
"""

from unittest import TestCase, skip
from chatterbot.conversation import Statement
from chatterbot import comparisons
from chatterbot import languages


class LevenshteinDistanceTestCase(TestCase):

    def setUp(self):
        super().setUp()

        self.compare = comparisons.LevenshteinDistance(
            language=languages.ENG
        )

    def test_levenshtein_distance_statement_false(self):
        """
        Falsy values should match by zero.
        """
        statement = Statement(text='')
        other_statement = Statement(text='Hello')

        value = self.compare(statement, other_statement)

        self.assertEqual(value, 0)

    def test_levenshtein_distance_other_statement_false(self):
        """
        Falsy values should match by zero.
        """
        statement = Statement(text='Hello')
        other_statement = Statement(text='')

        value = self.compare(statement, other_statement)

        self.assertEqual(value, 0)

    def test_levenshtein_distance_statement_integer(self):
        """
        Test that an exception is not raised if a statement is initialized
        with an integer value as its text attribute.
        """
        statement = Statement(text=2)
        other_statement = Statement(text='Hello')

        value = self.compare(statement, other_statement)

        self.assertEqual(value, 0)

    def test_exact_match_different_capitalization(self):
        """
        Test that text capitalization is ignored.
        """
        statement = Statement(text='Hi HoW ArE yOu?')
        other_statement = Statement(text='hI hOw are YoU?')

        value = self.compare(statement, other_statement)

        self.assertEqual(value, 1)


class SpacySimilarityTests(TestCase):

    def setUp(self):
        super().setUp()

        self.compare = comparisons.SpacySimilarity(
            language=languages.ENG
        )

    @skip('TODO: Update assertion & re-enable')
    def test_exact_match_different_stopwords(self):
        """
        Test sentences with different stopwords.
        """
        statement = Statement(text='What is matter?')
        other_statement = Statement(text='What is the matter?')

        value = self.compare(statement, other_statement)

        self.assertAlmostEqual(value, 0.7, places=1)

    def test_exact_match_different_capitalization(self):
        """
        Test that text capitalization is ignored.
        """
        statement = Statement(text='Hi HoW ArE yOu?')
        other_statement = Statement(text='hI hOw are YoU?')

        value = self.compare(statement, other_statement)

        self.assertAlmostEqual(value, 0.8, places=1)


class JaccardSimilarityTestCase(TestCase):

    def setUp(self):
        super().setUp()

        self.compare = comparisons.JaccardSimilarity(
            language=languages.ENG
        )

    def test_empty_token_sets_have_zero_similarity(self):
        for text_a, text_b in [('', ''), ('the', 'and'), ('is the', 'we are')]:
            with self.subTest(text_a=text_a, text_b=text_b):
                self.assertEqual(self.compare.compare_text(text_a, text_b), 0)

    def test_one_empty_token_set_has_zero_similarity(self):
        for text_a, text_b in [('', 'cat'), ('the', 'cat'), ('cat', 'and')]:
            with self.subTest(text_a=text_a, text_b=text_b):
                self.assertEqual(self.compare.compare_text(text_a, text_b), 0)

    def test_nonempty_token_sets_keep_their_jaccard_score(self):
        self.assertEqual(self.compare.compare_text('cat dog', 'cat'), 0.5)

    def test_exact_match_different_capitalization(self):
        """
        Test that text capitalization is ignored.
        """
        statement = Statement(text='Hi HoW ArE yOu?')
        other_statement = Statement(text='hI hOw are YoU?')

        value = self.compare(statement, other_statement)

        self.assertEqual(value, 1)
