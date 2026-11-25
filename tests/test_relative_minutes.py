from datetime import datetime, timedelta
from unittest import TestCase

from chatterbot import parsing


class RelativeMinuteTests(TestCase):
    def test_future_minutes_preserve_the_reference_time(self):
        base_date = datetime(2024, 2, 29, 23, 58, 30, 250000)
        for expression, minutes in (
            ('next minute', 1),
            ('next 5 minutes', 5),
            ('following twenty minutes', 20),
            ('Next 2 Mins', 2),
        ):
            with self.subTest(expression=expression):
                matches = parsing.datetime_parsing(expression, base_date)
                self.assertEqual(
                    [value for _, value, _ in matches],
                    [base_date + timedelta(minutes=minutes)],
                )

    def test_past_minutes_can_cross_midnight(self):
        base_date = datetime(2024, 3, 1, 0, 2, 30, 250000)
        for expression, minutes in (
            ('last minute', 1),
            ('previous 5 minutes', 5),
            ('last twenty mins', 20),
        ):
            with self.subTest(expression=expression):
                matches = parsing.datetime_parsing(expression, base_date)
                self.assertEqual(
                    [value for _, value, _ in matches],
                    [base_date - timedelta(minutes=minutes)],
                )

    def test_current_minute_boundaries(self):
        base_date = datetime(2024, 3, 1, 15, 45, 30, 250000)
        for expression, expected in (
            ('this minute', datetime(2024, 3, 1, 15, 45)),
            ('coming minute', datetime(2024, 3, 1, 15, 45)),
            ('end of the minute', datetime(2024, 3, 1, 15, 45, 59)),
        ):
            with self.subTest(expression=expression):
                self.assertEqual(
                    parsing.datetime_parsing(expression, base_date),
                    [(expression, expected, (0, len(expression)))],
                )

    def test_minute_duration_forms_keep_their_reference_time(self):
        base_date = datetime(2024, 3, 1, 15, 45, 30)
        for expression, minutes in (
            ('5 minutes from now', 5),
            ('5 minutes ago', -5),
        ):
            with self.subTest(expression=expression):
                self.assertEqual(
                    parsing.datetime_parsing(expression, base_date),
                    [(expression, base_date + timedelta(minutes=minutes), (0, len(expression)))],
                )
