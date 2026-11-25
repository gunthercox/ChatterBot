from datetime import datetime
from unittest import TestCase

from chatterbot import parsing


class AdverbCaseTests(TestCase):
    def setUp(self):
        self.base_date = datetime(2024, 3, 1, 15, 45)

    def test_standalone_adverbs_ignore_case(self):
        cases = (
            ('Tomorrow', datetime(2024, 3, 2)),
            ('TODAY', datetime(2024, 3, 1)),
            ('YeStErDaY', datetime(2024, 2, 29)),
            ('ToNiGhT', datetime(2024, 3, 1)),
            ('TONITE', datetime(2024, 3, 1)),
            ('tomorrow', datetime(2024, 3, 2)),
        )
        for word, expected in cases:
            with self.subTest(word=word):
                self.assertEqual(
                    parsing.datetime_parsing('Meet ' + word + '.', self.base_date),
                    [(word, expected, (5, 5 + len(word)))],
                )

    def test_adverb_with_time_keeps_original_text(self):
        expression = 'Tomorrow at 2PM'
        self.assertEqual(
            parsing.datetime_parsing('Call ' + expression + '.', self.base_date),
            [(expression, datetime(2024, 3, 2, 14), (5, 5 + len(expression)))],
        )

    def test_duration_anchors_ignore_case(self):
        cases = (
            ('2 days before YESTERDAY', datetime(2024, 2, 27)),
            ('3 days after Tomorrow', datetime(2024, 3, 5)),
            ('5 days before TODAY', datetime(2024, 2, 25)),
        )
        for expression, expected in cases:
            with self.subTest(expression=expression):
                self.assertEqual(
                    parsing.datetime_parsing(expression, self.base_date),
                    [(expression, expected, (0, len(expression)))],
                )
