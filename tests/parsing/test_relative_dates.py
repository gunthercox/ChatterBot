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


class LeapYearDurationTests(TestCase):
    def assert_parses(self, phrase, base, expected):
        text = 'Schedule it ' + phrase + '.'
        start = len('Schedule it ')
        self.assertEqual(
            parsing.datetime_parsing(text, base),
            [(phrase, expected, (start, start + len(phrase)))],
        )

    def test_year_durations_clamp_leap_day_in_both_directions(self):
        base = datetime(2024, 2, 29, 10, 30)
        for duration in ('ago', 'before', 'earlier'):
            with self.subTest(duration=duration):
                self.assert_parses('1 year ' + duration, base, datetime(2023, 2, 28))
        for duration in ('after', 'later', 'from now'):
            with self.subTest(duration=duration):
                self.assert_parses('1 year ' + duration, base, datetime(2025, 2, 28))

    def test_explicit_duration_anchor_and_time_are_preserved(self):
        self.assert_parses(
            '1 year before tomorrow', datetime(2024, 2, 28), datetime(2023, 2, 28),
        )
        self.assert_parses(
            '2 years from now at 5pm', datetime(2024, 2, 29), datetime(2026, 2, 28, 17),
        )

    def test_leap_target_and_zero_duration_keep_february_29(self):
        base = datetime(2024, 2, 29)
        for phrase, expected in (
            ('4 years from now', datetime(2028, 2, 29)),
            ('4 yrs ago', datetime(2020, 2, 29)),
            ('0 years from now', base),
        ):
            with self.subTest(phrase=phrase):
                self.assert_parses(phrase, base, expected)

    def test_century_leap_year_rules(self):
        for phrase, expected in (
            ('100 years from now', datetime(2100, 2, 28)),
            ('100 years ago', datetime(1900, 2, 28)),
            ('400 years from now', datetime(2400, 2, 29)),
        ):
            with self.subTest(phrase=phrase):
                self.assert_parses(phrase, datetime(2000, 2, 29), expected)

    def test_ordinary_dates_keep_their_day(self):
        for base, expected in (
            (datetime(2023, 2, 28), datetime(2024, 2, 28)),
            (datetime(2024, 12, 31), datetime(2025, 12, 31)),
        ):
            with self.subTest(base=base):
                self.assert_parses('1 year from now', base, expected)


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
