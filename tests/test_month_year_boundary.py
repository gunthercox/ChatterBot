from datetime import datetime
from unittest import TestCase

from chatterbot import parsing


class MonthYearBoundaryTests(TestCase):
    def setUp(self):
        self.base_date = datetime(2024, 3, 1, 15, 45)

    def test_month_and_year_are_not_shortened_to_a_day(self):
        cases = (
            ('June 2026', datetime(2026, 6, 1)),
            ('January 2025', datetime(2025, 1, 1)),
            ('Dec 1999', datetime(1999, 12, 1)),
            ('March-2031', datetime(2031, 3, 1)),
        )
        for expression, expected in cases:
            with self.subTest(expression=expression):
                self.assertEqual(
                    parsing.datetime_parsing('Meet in ' + expression + '.', self.base_date),
                    [(expression, expected, (8, 8 + len(expression)))],
                )

    def test_month_and_day_forms_keep_their_priority(self):
        cases = (
            ('June 5', datetime(2024, 6, 5)),
            ('June 5th', datetime(2024, 6, 5)),
            ('June 5 2026', datetime(2026, 6, 5)),
            ('Jan 2nd 2025 at 3pm', datetime(2025, 1, 2, 15)),
            ('March-05-2027', datetime(2027, 3, 5)),
        )
        for expression, expected in cases:
            with self.subTest(expression=expression):
                self.assertEqual(
                    parsing.datetime_parsing(expression, self.base_date),
                    [(expression, expected, (0, len(expression)))],
                )
