from datetime import datetime, timedelta
from unittest import TestCase

from chatterbot import parsing


class WordQuantityTests(TestCase):
    def setUp(self):
        self.base_date = datetime(2024, 3, 1, 15, 45)

    def test_scale_words_in_duration_expressions(self):
        cases = (
            ('one hundred days from now', timedelta(days=100)),
            ('two hundred days ago', timedelta(days=-200)),
            ('two thousand three hundred twenty one minutes from now', timedelta(minutes=2321)),
            ('one thousand one days from now', timedelta(days=1001)),
            (
                'nine hundred ninety nine thousand nine hundred ninety nine minutes from now',
                timedelta(minutes=999999),
            ),
        )
        for expression, offset in cases:
            with self.subTest(expression=expression):
                self.assertEqual(
                    parsing.datetime_parsing(expression, self.base_date),
                    [(expression, self.base_date + offset, (0, len(expression)))],
                )

    def test_teens_and_tens_are_complete_number_words(self):
        cases = (
            ('nineteen minutes from now', timedelta(minutes=19)),
            ('sixty minutes ago', timedelta(minutes=-60)),
            ('ninety-nine days from now', timedelta(days=99)),
            ('sixteen days ago', timedelta(days=-16)),
        )
        for expression, offset in cases:
            with self.subTest(expression=expression):
                self.assertEqual(
                    parsing.datetime_parsing(expression, self.base_date),
                    [(expression, self.base_date + offset, (0, len(expression)))],
                )

    def test_article_means_one(self):
        cases = (
            ('a day ago', timedelta(days=-1)),
            ('A week from now', timedelta(weeks=1)),
            ('a hundred minutes from now', timedelta(minutes=100)),
        )
        for expression, offset in cases:
            with self.subTest(expression=expression):
                self.assertEqual(
                    parsing.datetime_parsing(expression, self.base_date),
                    [(expression, self.base_date + offset, (0, len(expression)))],
                )

    def test_scale_words_in_relative_expressions(self):
        midnight = datetime(2024, 3, 1)
        for expression, offset in (
            ('next two hundred weeks', timedelta(weeks=200)),
            ('previous two hundred days', timedelta(days=-200)),
        ):
            with self.subTest(expression=expression):
                self.assertEqual(
                    parsing.datetime_parsing(expression, self.base_date),
                    [(expression, midnight + offset, (0, len(expression)))],
                )

    def test_number_conversion_preserves_simple_inputs(self):
        cases = (
            (None, 1), (0, 0), ('0', 0), (21, 21), ('21', 21),
            ('twenty-one', 21), ('twenty one', 21),
            ('sixteen', 16), ('seventeen', 17), ('eighteen', 18), ('nineteen', 19),
            ('sixty', 60), ('seventy', 70), ('eighty', 80), ('ninety', 90),
            ('hundred', 100), ('thousand', 1000), ('two hundred ten', 210),
            ('one hundred thousand', 100000), ('a', 1), ('A', 1),
        )
        for value, expected in cases:
            with self.subTest(value=value):
                self.assertEqual(parsing.convert_string_to_number(value), expected)
