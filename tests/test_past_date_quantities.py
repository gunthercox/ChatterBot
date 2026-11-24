from datetime import datetime
from unittest import TestCase

from chatterbot import parsing


class PastDateQuantityTests(TestCase):

    def test_past_offsets_use_numeric_and_word_quantities(self):
        base_date = datetime(2026, 1, 31, 15, 30)
        cases = [
            ('last 3 weeks', datetime(2026, 1, 10)),
            ('previous two weeks', datetime(2026, 1, 17)),
            ('previous 2 days', datetime(2026, 1, 29)),
            ('last two days', datetime(2026, 1, 29)),
            ('last 2 months', datetime(2025, 11, 30)),
            ('previous 14 months', datetime(2024, 11, 30)),
            ('last two years', datetime(2024, 1, 1)),
        ]
        for text, expected in cases:
            with self.subTest(text=text):
                result = parsing.datetime_parsing(text, base_date)

                self.assertEqual(len(result), 1)
                self.assertEqual(result[0][1], expected)

    def test_past_months_clamp_to_the_target_leap_month(self):
        result = parsing.datetime_parsing('last 13 months', datetime(2025, 3, 31))

        self.assertEqual(result[0][1], datetime(2024, 2, 29))

    def test_past_offsets_default_to_one_unit(self):
        base_date = datetime(2026, 1, 31, 15, 30)
        cases = [
            ('last day', datetime(2026, 1, 30)),
            ('previous week', datetime(2026, 1, 24)),
            ('last month', datetime(2025, 12, 31)),
            ('previous year', datetime(2025, 1, 1)),
        ]
        for text, expected in cases:
            with self.subTest(text=text):
                result = parsing.datetime_parsing(text, base_date)

                self.assertEqual(result[0][1], expected)
