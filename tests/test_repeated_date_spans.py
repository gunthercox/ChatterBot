from datetime import datetime
from unittest import TestCase

from chatterbot import parsing


class RepeatedDateSpanTests(TestCase):
    def setUp(self):
        self.base_date = datetime(2024, 3, 1)

    def test_repeated_adverbs_retain_each_occurrence(self):
        self.assertEqual(
            parsing.datetime_parsing('today and today', self.base_date),
            [
                ('today', self.base_date, (0, 5)),
                ('today', self.base_date, (10, 15)),
            ],
        )

    def test_repeated_weekdays_retain_each_occurrence(self):
        self.assertEqual(
            parsing.datetime_parsing('Monday then Monday', self.base_date),
            [
                ('Monday', datetime(2024, 3, 4), (0, 6)),
                ('Monday', datetime(2024, 3, 4), (12, 18)),
            ],
        )

    def test_repeated_full_dates_suppress_nested_matches(self):
        self.assertEqual(
            parsing.datetime_parsing('June 5 2026 and June 5 2026', self.base_date),
            [
                ('June 5 2026', datetime(2026, 6, 5), (0, 11)),
                ('June 5 2026', datetime(2026, 6, 5), (16, 27)),
            ],
        )

    def test_standalone_year_uses_its_own_span(self):
        self.assertEqual(
            parsing.datetime_parsing('June 5 2026 and 2026', self.base_date),
            [
                ('June 5 2026', datetime(2026, 6, 5), (0, 11)),
                ('2026', datetime(2026, 1, 1), (16, 20)),
            ],
        )

    def test_longer_expression_keeps_priority_at_each_position(self):
        self.assertEqual(
            parsing.datetime_parsing('today; today at 2pm; today', self.base_date),
            [
                ('today', self.base_date, (0, 5)),
                ('today at 2pm', datetime(2024, 3, 1, 14), (7, 19)),
                ('today', self.base_date, (21, 26)),
            ],
        )

    def test_repeated_quarter_ranges_retain_each_occurrence(self):
        expression = 'first quarter of 2024'
        quarter = [datetime(2024, 1, 1), datetime(2024, 3, 31)]
        self.assertEqual(
            parsing.datetime_parsing(expression + ' and ' + expression, self.base_date),
            [
                (expression, quarter, (0, len(expression))),
                (expression, quarter, (len(expression) + 5, 2 * len(expression) + 5)),
            ],
        )

    def test_equal_dates_from_different_phrases_remain_separate(self):
        self.assertEqual(
            parsing.datetime_parsing('today and this day', self.base_date),
            [
                ('today', self.base_date, (0, 5)),
                ('this day', self.base_date, (10, 18)),
            ],
        )
