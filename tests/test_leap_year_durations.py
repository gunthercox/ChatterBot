from datetime import datetime
from unittest import TestCase

from chatterbot.parsing import datetime_parsing


class LeapYearDurationTests(TestCase):
    def assert_parses(self, phrase, base, expected):
        text = 'Schedule it ' + phrase + '.'
        start = len('Schedule it ')
        self.assertEqual(
            datetime_parsing(text, base),
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
