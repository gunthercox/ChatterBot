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


class TimeOfDayParsingTests(TestCase):
    def test_captured_pattern_has_am(self):

        input_text = 'You have to woke up at 5 am in the morning'

        parser = parsing.datetime_parsing(input_text)

        self.assertIn('5 am', parser[0])

        self.assertEqual(parser[0][1].strftime('%d'), datetime.today().strftime('%d'))

        self.assertEqual(parser[0][1].strftime('%H'), '05')

        self.assertEqual(len(parser), 1)

    def test_captured_pattern_has_am_case_insensitive_1(self):

        input_text = '7 AM'

        parser = parsing.datetime_parsing(input_text)

        self.assertIn('7 AM', parser[0])

        self.assertEqual(parser[0][1].strftime('%d'), datetime.today().strftime('%d'))

        self.assertEqual(parser[0][1].strftime('%H'), '07')

        self.assertEqual(len(parser), 1)

    def test_captured_pattern_has_am_case_insensitive_2(self):

        input_text = '1 Am'

        parser = parsing.datetime_parsing(input_text)

        self.assertIn('1 Am', parser[0])

        self.assertEqual(parser[0][1].strftime('%d'), datetime.today().strftime('%d'))

        self.assertEqual(parser[0][1].strftime('%H'), '01')

        self.assertEqual(len(parser), 1)

    def test_captured_pattern_has_am_case_insensitive_3(self):

        input_text = '9aM'

        parser = parsing.datetime_parsing(input_text)

        self.assertIn('9aM', parser[0])

        self.assertEqual(parser[0][1].strftime('%d'), datetime.today().strftime('%d'))

        self.assertEqual(parser[0][1].strftime('%H'), '09')

        self.assertEqual(len(parser), 1)

    def test_captured_pattern_has_pm(self):

        input_text = 'Your dental appointment at 4 pm in the evening.'

        parser = parsing.datetime_parsing(input_text)

        self.assertIn('4 pm', parser[0])

        self.assertEqual(parser[0][1].strftime('%d'), datetime.today().strftime('%d'))

        self.assertEqual(parser[0][1].strftime('%H'), '16')

        self.assertEqual(len(parser), 1)

    def test_captured_pattern_has_pm_case_insensitive_1(self):

        input_text = '8 PM'

        parser = parsing.datetime_parsing(input_text)

        self.assertIn('8 PM', parser[0])

        self.assertEqual(parser[0][1].strftime('%d'), datetime.today().strftime('%d'))

        self.assertEqual(parser[0][1].strftime('%H'), '20')

        self.assertEqual(len(parser), 1)

    def test_captured_pattern_has_pm_case_insensitive_2(self):

        input_text = '11 pM'

        parser = parsing.datetime_parsing(input_text)

        self.assertIn('11 pM', parser[0])

        self.assertEqual(parser[0][1].strftime('%d'), datetime.today().strftime('%d'))

        self.assertEqual(parser[0][1].strftime('%H'), '23')

        self.assertEqual(len(parser), 1)

    def test_captured_pattern_has_pm_case_insensitive_3(self):

        input_text = '3Pm'

        parser = parsing.datetime_parsing(input_text)

        self.assertIn('3Pm', parser[0])

        self.assertEqual(parser[0][1].strftime('%d'), datetime.today().strftime('%d'))

        self.assertEqual(parser[0][1].strftime('%H'), '15')

        self.assertEqual(len(parser), 1)

    def test_today_at_time_uses_base_date(self):

        """

        The string 'today at [time]' should respect the base_date parameter.

        """

        base_date = datetime(2018, 7, 14, 8, 52, 21)  # July 14, 2018 at 8:52:21 AM

        input_text = 'Your dental appointment is scheduled today at 9:00pm.'

        parser = parsing.datetime_parsing(input_text, base_date)

        self.assertEqual(len(parser), 1)

        self.assertIn('today at 9:00pm', parser[0])

        parsed_datetime = parser[0][1]

        # Should be July 14, 2018 at 9:00 PM

        self.assertEqual(parsed_datetime.year, 2018)

        self.assertEqual(parsed_datetime.month, 7)

        self.assertEqual(parsed_datetime.day, 14)

        self.assertEqual(parsed_datetime.hour, 21)  # 9 PM

        self.assertEqual(parsed_datetime.minute, 0)

    def test_noon_without_convention(self):

        """

        Test '12:00' without AM/PM defaults to AM convention (midnight = 0)

        """

        base_date = datetime(2025, 10, 18, 0, 0, 0)

        input_text = 'Meeting at 12:00'

        parser = parsing.datetime_parsing(input_text, base_date)

        self.assertEqual(len(parser), 1)

        # No convention defaults to 'am', so 12:00 becomes 0 (midnight)

        self.assertEqual(parser[0][1].hour, 0)

        self.assertEqual(parser[0][1].minute, 0)

    def test_twelve_pm(self):

        """

        Test '12:00 pm' is noon (stays as 12)

        """

        base_date = datetime(2025, 10, 18, 0, 0, 0)

        input_text = 'Meeting at 12:00 pm'

        parser = parsing.datetime_parsing(input_text, base_date)

        self.assertEqual(len(parser), 1)

        self.assertEqual(parser[0][1].hour, 12)

        self.assertEqual(parser[0][1].minute, 0)

    def test_twelve_am(self):

        """

        Test '12:00 am' is midnight (converted to 0)

        """

        base_date = datetime(2025, 10, 18, 0, 0, 0)

        input_text = 'Meeting at 12:00 am'

        parser = parsing.datetime_parsing(input_text, base_date)

        self.assertEqual(len(parser), 1)

        self.assertEqual(parser[0][1].hour, 0)

        self.assertEqual(parser[0][1].minute, 0)

    def test_one_am(self):

        """

        Test '1:00 am' is 1:00

        """

        base_date = datetime(2025, 10, 18, 0, 0, 0)

        input_text = 'Meeting at 1:00 am'

        parser = parsing.datetime_parsing(input_text, base_date)

        self.assertEqual(len(parser), 1)

        self.assertEqual(parser[0][1].hour, 1)

        self.assertEqual(parser[0][1].minute, 0)

    def test_one_pm(self):

        """

        Test '1:00 pm' is 13:00

        """

        base_date = datetime(2025, 10, 18, 0, 0, 0)

        input_text = 'Meeting at 1:00 pm'

        parser = parsing.datetime_parsing(input_text, base_date)

        self.assertEqual(len(parser), 1)

        self.assertEqual(parser[0][1].hour, 13)

        self.assertEqual(parser[0][1].minute, 0)
