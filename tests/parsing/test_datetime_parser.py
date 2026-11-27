from datetime import datetime, timedelta
from unittest import TestCase

from chatterbot import parsing


class DateTimeParsingFunctionIntegrationTestCases(TestCase):
    """
    Test the datetime parsing module.

    Output of the parser is an array of tuples
    [match, value, (start, end)]
    """

    def setUp(self):
        super().setUp()
        self.base_date = datetime.now()

    def test_captured_pattern_is_on_date(self):
        input_text = 'The event is on Monday 12 January 2012'
        parser = parsing.datetime_parsing(input_text)
        self.assertIn('Monday 12 January 2012', parser[0])
        self.assertEqual(parser[0][1], datetime(2012, 1, 12))
        self.assertEqual(len(parser), 1)

    def test_captured_pattern_this_weekday(self):
        input_text = 'This monday'
        parser = parsing.datetime_parsing(input_text)
        self.assertIn(input_text, parser[0])
        self.assertEqual(
            parser[0][1].strftime('%d-%m-%y'),
            parsing.this_week_day(self.base_date, 0).strftime('%d-%m-%y')
        )
        self.assertEqual(len(parser), 1)

    def test_captured_pattern_last_weekday(self):
        input_text = 'Last monday'
        parser = parsing.datetime_parsing(input_text)
        self.assertIn(input_text, parser[0])
        self.assertEqual(
            parser[0][1].strftime('%d-%m-%y'),
            parsing.previous_week_day(self.base_date, 0).strftime('%d-%m-%y')
        )
        self.assertEqual(len(parser), 1)

    def test_captured_pattern_next_weekday(self):
        input_text = 'Next monday'
        parser = parsing.datetime_parsing(input_text)
        self.assertIn(input_text, parser[0])
        self.assertEqual(
            parser[0][1].strftime('%d-%m-%y'),
            parsing.next_week_day(self.base_date, 0).strftime('%d-%m-%y')
        )
        self.assertEqual(len(parser), 1)

    def test_captured_pattern_minutes_from_now(self):
        input_text = '25 minutes from now'
        parser = parsing.datetime_parsing(input_text)
        self.assertIn(input_text, parser[0])
        self.assertEqual(
            parser[0][1].strftime('%d-%m-%y'),
            parsing.date_from_duration(
                self.base_date, 25, 'minutes', 'from now'
            ).strftime('%d-%m-%y')
        )
        self.assertEqual(len(parser), 1)

    def test_captured_pattern_days_later(self):
        input_text = '10 days later'
        parser = parsing.datetime_parsing(input_text)
        self.assertIn(input_text, parser[0])
        self.assertEqual(
            parser[0][1].strftime('%d-%m-%y'),
            parsing.date_from_duration(self.base_date, 10, 'days', 'later').strftime('%d-%m-%y')
        )
        self.assertEqual(len(parser), 1)

    def test_captured_pattern_year(self):
        input_text = '2010'
        parser = parsing.datetime_parsing(input_text)
        self.assertIn(input_text, parser[0])
        self.assertEqual(parser[0][1].strftime('%Y'), input_text)
        self.assertEqual(len(parser), 1)

    def test_captured_pattern_today(self):
        input_text = 'today'
        parser = parsing.datetime_parsing(input_text)
        self.assertIn(input_text, parser[0])
        self.assertEqual(parser[0][1].strftime('%d'), datetime.today().strftime('%d'))
        self.assertEqual(len(parser), 1)

    def test_captured_pattern_tomorrow(self):
        input_text = 'tomorrow'
        parser = parsing.datetime_parsing(input_text)
        self.assertIn(input_text, parser[0])
        self.assertEqual(
            parser[0][1].strftime('%d'),
            (datetime.today() + timedelta(days=1)).strftime('%d')
        )
        self.assertEqual(len(parser), 1)

    def test_captured_pattern_yesterday(self):
        input_text = 'yesterday'
        parser = parsing.datetime_parsing(input_text)
        self.assertIn(input_text, parser[0])
        self.assertEqual(
            parser[0][1].strftime('%d'),
            (datetime.today() - timedelta(days=1)).strftime('%d')
        )
        self.assertEqual(len(parser), 1)

    def test_captured_pattern_before_yesterday(self):
        input_text = 'day before yesterday'
        parser = parsing.datetime_parsing(input_text)
        self.assertIn(input_text, parser[0])
        self.assertEqual(
            parser[0][1].strftime('%d'),
            (datetime.today() - timedelta(days=2)).strftime('%d')
        )
        self.assertEqual(len(parser), 1)

    def test_captured_pattern_before_today(self):
        input_text = 'day before today'
        parser = parsing.datetime_parsing(input_text)
        self.assertIn(input_text, parser[0])
        self.assertEqual(
            parser[0][1].strftime('%d'),
            (datetime.today() - timedelta(days=1)).strftime('%d')
        )
        self.assertEqual(len(parser), 1)

    def test_captured_pattern_before_tomorrow(self):
        input_text = 'day before tomorrow'
        parser = parsing.datetime_parsing(input_text)
        self.assertIn(input_text, parser[0])
        self.assertEqual(
            parser[0][1].strftime('%d'),
            (datetime.today() - timedelta(days=0)).strftime('%d')
        )
        self.assertEqual(len(parser), 1)

        input_text = '2 days before'
        parser = parsing.datetime_parsing(input_text)
        self.assertIn(input_text, parser[0])
        self.assertEqual(
            parser[0][1].strftime('%d'),
            (datetime.today() - timedelta(days=2)).strftime('%d')
        )
        self.assertEqual(len(parser), 1)

    def test_captured_pattern_two_days(self):
        input_text = 'Monday and Friday'
        parser = parsing.datetime_parsing(input_text)
        self.assertIn('Monday', parser[0])
        self.assertIn('Friday', parser[1])
        self.assertEqual(
            parser[0][1].strftime('%d'),
            parsing.this_week_day(self.base_date, 0).strftime('%d')
        )
        self.assertEqual(
            parser[1][1].strftime('%d'),
            parsing.this_week_day(self.base_date, 4).strftime('%d')
        )
        self.assertEqual(len(parser), 2)

    def test_captured_pattern_first_quarter_of_year(self):
        input_text = 'First quarter of 2016'
        parser = parsing.datetime_parsing(input_text)
        self.assertIn(input_text, parser[0])
        self.assertEqual(parser[0][1][0].strftime('%d-%m-%Y'), '01-01-2016')
        self.assertEqual(parser[0][1][1].strftime('%d-%m-%Y'), '31-03-2016')
        self.assertEqual(len(parser), 1)

    def test_captured_pattern_last_quarter_of_year(self):
        input_text = 'Last quarter of 2015'
        parser = parsing.datetime_parsing(input_text)
        self.assertIn(input_text, parser[0])
        self.assertEqual(parser[0][1][0].strftime('%d-%m-%Y'), '01-10-2015')
        self.assertEqual(parser[0][1][1].strftime('%d-%m-%Y'), '31-12-2015')
        self.assertEqual(len(parser), 1)

    def test_calendar_quarter_boundaries(self):
        quarters = [
            ('First', datetime(2016, 1, 1), datetime(2016, 3, 31)),
            ('Second', datetime(2016, 4, 1), datetime(2016, 6, 30)),
            ('Third', datetime(2016, 7, 1), datetime(2016, 9, 30)),
            ('Fourth', datetime(2016, 10, 1), datetime(2016, 12, 31)),
            ('Last', datetime(2016, 10, 1), datetime(2016, 12, 31)),
        ]
        for ordinal, start, end in quarters:
            with self.subTest(quarter=ordinal):
                input_text = f'{ordinal} quarter of 2016'
                result = parsing.datetime_parsing(input_text, self.base_date)

                self.assertEqual(len(result), 1)
                self.assertEqual(result[0][0], input_text)
                self.assertEqual(result[0][1], [start, end])

    def test_captured_pattern_is_next_three_weeks(self):
        input_text = 'Next 3 weeks'
        parser = parsing.datetime_parsing(input_text)
        self.assertIn(input_text, parser[0])
        self.assertEqual(
            parser[0][1].strftime('%d-%m-%Y'),
            (datetime.today() + timedelta(weeks=3)).strftime('%d-%m-%Y')
        )
        self.assertEqual(len(parser), 1)

    def test_captured_pattern_is_next_x_weeks_case_insensitive(self):
        input_text = 'next 2 Weeks'
        parser = parsing.datetime_parsing(input_text)
        self.assertIn(input_text, parser[0])
        self.assertEqual(
            parser[0][1].strftime('%d-%m-%Y'),
            (datetime.today() + timedelta(weeks=2)).strftime('%d-%m-%Y')
        )
        self.assertEqual(len(parser), 1)

    def test_captured_pattern_is_next_eight_days(self):
        input_text = 'Next 8 days'
        parser = parsing.datetime_parsing(input_text)
        self.assertIn(input_text, parser[0])
        self.assertEqual(
            parser[0][1].strftime('%d-%m-%Y'),
            (datetime.today() + timedelta(days=8)).strftime('%d-%m-%Y')
        )
        self.assertEqual(len(parser), 1)

    def test_captured_pattern_is_next_x_days_case_insensitive(self):
        input_text = 'next 14 Days'
        parser = parsing.datetime_parsing(input_text)
        self.assertIn(input_text, parser[0])
        self.assertEqual(
            parser[0][1].strftime('%d-%m-%Y'),
            (datetime.today() + timedelta(days=14)).strftime('%d-%m-%Y')
        )
        self.assertEqual(len(parser), 1)

    def test_captured_pattern_is_next_ten_years(self):
        input_text = 'Next 10 years'
        parser = parsing.datetime_parsing(input_text)
        self.assertIn('Next 10 year', parser[0])
        self.assertEqual(
            parser[0][1].strftime('%d-%m-%Y'),
            (datetime.today() + timedelta(10 * 365)).strftime('%d-%m-%Y')
        )
        self.assertEqual(len(parser), 1)

    def test_captured_pattern_is_next_x_years_case_insensitive(self):
        input_text = 'next 43 Years'
        parser = parsing.datetime_parsing(input_text)
        self.assertIn('next 43 Year', parser[0])
        self.assertEqual(
            parser[0][1].strftime('%d-%m-%Y'),
            (datetime.today() + timedelta(43 * 365)).strftime('%d-%m-%Y')
        )
        self.assertEqual(len(parser), 1)

    def test_captured_pattern_is_next_eleven_months(self):
        import calendar
        input_text = 'Next 11 months'
        parser = parsing.datetime_parsing(input_text)
        relative_date = datetime.today()
        month = relative_date.month - 1 + 11
        year = relative_date.year + month // 12
        month = month % 12 + 1
        day = min(relative_date.day, calendar.monthrange(year, month)[1])
        self.assertIn('Next 11 month', parser[0])
        self.assertEqual(
            parser[0][1].strftime('%d-%m-%Y'), datetime(year, month, day).strftime('%d-%m-%Y')
        )
        self.assertEqual(len(parser), 1)

    def test_captured_pattern_is_next_x_months_case_insensitive(self):
        import calendar
        input_text = 'next 55 Months'
        parser = parsing.datetime_parsing(input_text)
        relative_date = datetime.today()
        month = relative_date.month - 1 + 55
        year = relative_date.year + month // 12
        month = month % 12 + 1
        day = min(relative_date.day, calendar.monthrange(year, month)[1])
        self.assertIn('next 55 Month', parser[0])
        self.assertEqual(
            parser[0][1].strftime('%d-%m-%Y'), datetime(year, month, day).strftime('%d-%m-%Y')
        )
        self.assertEqual(len(parser), 1)

    def test_captured_pattern_is_on_day(self):
        input_text = 'My birthday is on January 2nd.'
        parser = parsing.datetime_parsing(input_text)
        self.assertIn('January 2nd', parser[0])
        self.assertEqual(parser[0][1].month, 1)
        self.assertEqual(parser[0][1].day, 2)
        self.assertEqual(len(parser), 1)

    def test_captured_pattern_is_on_day_of_year_variation1(self):
        input_text = 'My birthday is on January 1st 2014.'
        parser = parsing.datetime_parsing(input_text)
        self.assertIn('January 1st 2014', parser[0])
        self.assertEqual(parser[0][1].strftime('%d-%m-%Y'), '01-01-2014')
        self.assertEqual(len(parser), 1)

    def test_captured_pattern_is_on_day_of_year_variation2(self):
        input_text = 'My birthday is on 2nd January 2014.'
        parser = parsing.datetime_parsing(input_text)
        self.assertIn('2nd January 2014', parser[0])
        self.assertEqual(parser[0][1].strftime('%d-%m-%Y'), '02-01-2014')
        self.assertEqual(len(parser), 1)


class DateTimeParsingTestCases(TestCase):
    """
    Unit tests for datetime parsing functions.
    """

    def test_next_week_day(self):
        base_date = datetime(2016, 12, 7, 10, 10, 52, 85280)
        weekday = 2  # Wednesday
        result = parsing.next_week_day(base_date, weekday)

        self.assertEqual(result, datetime(2016, 12, 14, 10, 10, 52, 85280))

    def test_previous_week_day(self):
        base_date = datetime(2016, 12, 14, 10, 10, 52, 85280)
        weekday = 2  # Wednesday
        result = parsing.previous_week_day(base_date, weekday)

        self.assertEqual(result, datetime(2016, 12, 7, 10, 10, 52, 85280))

    def test_this_week_day_before_day(self):
        base_date = datetime(2016, 12, 5, 10, 10, 52, 85280)  # Monday
        weekday = 2  # Wednesday
        result = parsing.this_week_day(base_date, weekday)

        self.assertEqual(result, datetime(2016, 12, 7, 10, 10, 52, 85280))

    def test_this_week_day_after_day(self):
        base_date = datetime(2016, 12, 9, 10, 10, 52, 85280)  # Friday
        weekday = 2  # Wednesday
        result = parsing.this_week_day(base_date, weekday)

        self.assertEqual(result, datetime(2016, 12, 14, 10, 10, 52, 85280))

    def test_next_month_from_january_31st(self):
        """
        Test 'next month' from Jan 31 handles February correctly
        """
        base_date = datetime(2025, 1, 31, 12, 0, 0)
        input_text = 'next month'
        parser = parsing.datetime_parsing(input_text, base_date)

        self.assertEqual(len(parser), 1)
        # February only has 28 days in 2025, should clamp to last valid day
        self.assertEqual(parser[0][1].year, 2025)
        self.assertEqual(parser[0][1].month, 2)
        self.assertEqual(parser[0][1].day, 28)

    def test_next_3_months_crosses_year_boundary(self):
        """
        Test 'next 3 months' crossing year boundary
        """
        base_date = datetime(2025, 11, 15, 12, 0, 0)
        input_text = 'next 3 months'
        parser = parsing.datetime_parsing(input_text, base_date)

        self.assertEqual(len(parser), 1)
        self.assertEqual(parser[0][1].year, 2026)
        self.assertEqual(parser[0][1].month, 2)
        self.assertEqual(parser[0][1].day, 15)

    def test_next_month_from_march_31st(self):
        """
        Test 'next month' from March 31 handles April correctly
        """
        base_date = datetime(2025, 3, 31, 12, 0, 0)
        input_text = 'next month'
        parser = parsing.datetime_parsing(input_text, base_date)

        self.assertEqual(len(parser), 1)
        # April only has 30 days, should pick the last valid day
        self.assertEqual(parser[0][1].year, 2025)
        self.assertEqual(parser[0][1].month, 4)
        self.assertEqual(parser[0][1].day, 30)

    def test_next_month_from_may_31st(self):
        """
        Test 'next month' from May 31 handles June correctly
        """
        base_date = datetime(2025, 5, 31, 12, 0, 0)
        input_text = 'next month'
        parser = parsing.datetime_parsing(input_text, base_date)

        self.assertEqual(len(parser), 1)
        # June only has 30 days, should pick the last valid day
        self.assertEqual(parser[0][1].year, 2025)
        self.assertEqual(parser[0][1].month, 6)
        self.assertEqual(parser[0][1].day, 30)

    def test_last_month_from_january(self):
        """
        Test 'last month' from January rolls back to December of the previous year
        """
        base_date = datetime(2025, 1, 15, 12, 0, 0)
        input_text = 'last month'
        parser = parsing.datetime_parsing(input_text, base_date)

        self.assertEqual(len(parser), 1)
        self.assertEqual(parser[0][1].year, 2024)
        self.assertEqual(parser[0][1].month, 12)
        self.assertEqual(parser[0][1].day, 15)

    def test_last_month_from_march_31st(self):
        """
        Test 'last month' from March 31 handles February correctly
        """
        base_date = datetime(2025, 3, 31, 12, 0, 0)
        input_text = 'last month'
        parser = parsing.datetime_parsing(input_text, base_date)

        self.assertEqual(len(parser), 1)
        # February only has 28 days in 2025, should clamp to last valid day
        self.assertEqual(parser[0][1].year, 2025)
        self.assertEqual(parser[0][1].month, 2)
        self.assertEqual(parser[0][1].day, 28)

    def test_end_of_the_week(self):
        """
        Test 'end of the week' returns the Sunday of the current week
        """
        base_date = datetime(2025, 6, 11, 12, 0, 0)  # Wednesday
        input_text = 'end of the week'
        parser = parsing.datetime_parsing(input_text, base_date)

        self.assertEqual(len(parser), 1)
        self.assertEqual(parser[0][1], datetime(2025, 6, 15))

    def test_multiple_datetime_expressions(self):
        """
        Test parsing text with multiple date/time references
        """
        base_date = datetime(2025, 10, 18, 12, 0, 0)
        input_text = 'Meeting today at 2pm and tomorrow at 3pm'
        parser = parsing.datetime_parsing(input_text, base_date)

        self.assertEqual(len(parser), 2)
        # First: today at 2pm
        self.assertEqual(parser[0][1].year, 2025)
        self.assertEqual(parser[0][1].month, 10)
        self.assertEqual(parser[0][1].day, 18)
        self.assertEqual(parser[0][1].hour, 14)
        # Second: tomorrow at 3pm
        self.assertEqual(parser[1][1].year, 2025)
        self.assertEqual(parser[1][1].month, 10)
        self.assertEqual(parser[1][1].day, 19)
        self.assertEqual(parser[1][1].hour, 15)

    def test_duration_from_yesterday(self):
        """
        Test '2 days after yesterday' using base_time
        """
        base_date = datetime(2025, 10, 18, 12, 0, 0)
        input_text = '2 days after yesterday'
        parser = parsing.datetime_parsing(input_text, base_date)

        self.assertEqual(len(parser), 1)
        # Yesterday = Oct 17, + 2 days = Oct 19
        self.assertEqual(parser[0][1].year, 2025)
        self.assertEqual(parser[0][1].month, 10)
        self.assertEqual(parser[0][1].day, 19)

    def test_duration_from_tomorrow(self):
        """
        Test '3 days after tomorrow'
        """
        base_date = datetime(2025, 10, 18, 12, 0, 0)
        input_text = '3 days after tomorrow'
        parser = parsing.datetime_parsing(input_text, base_date)

        self.assertEqual(len(parser), 1)
        # Tomorrow = Oct 19, + 3 days = Oct 22
        self.assertEqual(parser[0][1].year, 2025)
        self.assertEqual(parser[0][1].month, 10)
        self.assertEqual(parser[0][1].day, 22)

    def test_duration_from_today(self):
        """
        Test '5 days before today'
        """
        base_date = datetime(2025, 10, 18, 12, 0, 0)
        input_text = '5 days before today'
        parser = parsing.datetime_parsing(input_text, base_date)

        self.assertEqual(len(parser), 1)
        # Today = Oct 18, - 5 days = Oct 13
        self.assertEqual(parser[0][1].year, 2025)
        self.assertEqual(parser[0][1].month, 10)
        self.assertEqual(parser[0][1].day, 13)
