import re
from datetime import timedelta, date, datetime
import calendar

# Variations of dates that the parser can capture
year_variations = ['year', 'years', 'yrs']
day_variations = ['days', 'day']
minute_variations = ['minute', 'minutes', 'mins']
week_variations = ['weeks', 'week', 'wks']

# Variables used for RegEx Matching
day_names = 'monday|tuesday|wednesday|thursday|friday|saturday|sunday'
month_names = 'january|february|march|april|may|june|july|august|september|october|november|december|jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec'
day_nearest_names = 'today|yesterday|tomorrow|tonight|tonite'
numbers = "(^a(?=\s)|one|two|three|four|five|six|seven|eight|nine|ten| \
                    eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen| \
                    eighteen|nineteen|twenty|thirty|forty|fifty|sixty|seventy|eighty| \
                    ninety|hundred|thousand)"
re_dmy = '(' + "|".join(day_variations + minute_variations + year_variations + week_variations) + ')'
re_duration = '(before|after|earlier|later|ago|from\snow)'
re_year = "(?<=\s)\d{4}|^\d{4}"
re_timeframe = 'this|next|following|previous|last'
re_ordinal = 'st|nd|rd|th|first|second|third|fourth|fourth|' + re_timeframe

# A list tuple of regular expressions / parser fn to match
# The order of the match in this list matters, So always start with the widest match and narrow it down
regex = [
    (re.compile(
        r'''
        (
            (?P<dow>%s) # day_names
            [,\s]\s*(?P<day>\d{1,2}) # Any digit
            \s+ # One or more space
            (?P<month>%s) # Month names
            \s+ # One or more space
            (?P<year>%s) # Year
        )
        '''% (day_names, month_names, re_year),
        (re.VERBOSE | re.IGNORECASE)
        ),
        lambda (m, base_date): datetime(
                int(m.group('year')),
                hashmonths[m.group('month').lower()],
                int(m.group('day'))
            )
    ),
    (re.compile(
        r'''
        (
            (?P<day>\d{1,2}) # Matches a digit
            [-\s] # One or more space
            (?P<month>%s) # Matches any month name
            [-\s] # Space
            (?P<year>\d{4}) # Year
        )
        '''% (month_names),
        (re.VERBOSE | re.IGNORECASE)
        ),
        lambda (m, base_date): datetime(
                int(m.group('year') if m.group('year') else base_date.year),
                hashmonths[m.group('month').strip().lower()],
                int(m.group('day') if m.group('day') else 1)
            )
    ),
    (re.compile(
        r'''
        (
            (?P<month>%s) # Matches any month name
            [-\s] # One or more space
            (?P<day>\d{1,2}) # Matches a digit
            (,\s)? # Space
            [-\s]?
            (?P<year>\d{4}) # Year
        )
        '''% (month_names),
        (re.VERBOSE | re.IGNORECASE)
        ),
        lambda (m, base_date): datetime(
                int(m.group('year') if m.group('year') else base_date.year),
                hashmonths[m.group('month').strip().lower()],
                int(m.group('day') if m.group('day') else 1)
            )
    ),
    (re.compile(
        r'''
        (
            ((?P<number>\d+|(%s[-\s]?)+)\s)? # Matches any number or string 25 or twenty five
            (?P<unit>%s)s?\s # Matches days, months, years, weeks, minutes
            (?P<duration>%s) # before, after, earlier, later, ago, from now
            (\s*(?P<base_time>(%s)))?
        )
        '''% (numbers, re_dmy, re_duration, day_nearest_names),
        (re.VERBOSE | re.IGNORECASE)
        ),
        lambda (m, base_date): dateFromDuration(
            base_date,
            m.group('number'),
            m.group('unit').lower(),
            m.group('duration').lower(),
            m.group('base_time')
        )
    ),
    (re.compile(
        r'''
        (?P<time>%s) # this, next, following, previous, last
        \s+
        (?P<dow>%s) # mon - fri
        '''% (re_timeframe, day_names),
        (re.VERBOSE | re.IGNORECASE),
        ),
        lambda (m, base_date): dateFromRelativeDay(base_date, m.group('time'), m.group('dow'))
    ),
    (re.compile(
        r'''
        (
            (?P<ordinal>%s) # First quarter of 2014
            \s+
            quarter\sof
            \s?
            (?P<year>%s)
        )
        '''% (re_ordinal, re_year),
        (re.VERBOSE | re.IGNORECASE)
        ),
        lambda (m, base_date): dateFromQuarter(
            base_date,
            hashordinals[m.group('ordinal').lower()],
            int(m.group('year') if m.group('year') else base.year)
        )
    ),
    (re.compile(
        r'''
        (
            (?P<ordinal_value>\d+)
            (?P<ordinal>%s) # 1st January 2012
            \s+
            (?P<month>%s)
            \s?
            (?P<year>%s)?
        )
        '''% (re_ordinal, month_names, re_year),
        (re.VERBOSE | re.IGNORECASE)
        ),
        lambda (m, base_date): datetime(
                int(m.group('year') if m.group('year') else base_date.year),
                int(hashmonths[m.group('month').lower()] if m.group('month') else 1),
                int(m.group('ordinal_value') if m.group('ordinal_value') else 1),
            )
    ),
    (re.compile(
        r'''
        (
            (?P<month>%s)
            \s+
            (?P<ordinal_value>\d+)
            (?P<ordinal>%s) # January 1st 2012
            \s?
            (?P<year>%s)?
        )
        '''% (month_names, re_ordinal, re_year),
        (re.VERBOSE | re.IGNORECASE)
        ),
        lambda (m, base_date): datetime(
                int(m.group('year') if m.group('year') else base_date.year),
                int(hashmonths[m.group('month').lower()] if m.group('month') else 1),
                int(m.group('ordinal_value') if m.group('ordinal_value') else 1),
            )
    ),
    (re.compile(
        r'''
        (?P<time>%s) # this, next, following, previous, last
        \s+
        (?P<dmy>%s) # year, day, week, month, night, minute, min
        '''% (re_timeframe, re_dmy),
        (re.VERBOSE | re.IGNORECASE),
        ),
        lambda (m, base_date): dateFromRelativeWeekYear(base_date, m.group('time'), m.group('dmy'))
    ),
    (re.compile(
        r'''
        (
            (?P<day>\d{1,2}) # Matches a digit 12 January
            [-\s] # One or more space
            (?P<month>%s)
        )
        '''% (month_names),
        (re.VERBOSE | re.IGNORECASE)
        ),
        lambda (m, base_date): datetime(
                base_date.year,
                hashmonths[m.group('month').strip().lower()],
                int(m.group('day') if m.group('day') else 1)
            )
    ),
    (re.compile(
        r'''
        (
            (?P<month>%s)
            [-\s] # One or more space
            (?P<day>\d{1,2}) # Matches a digit January 12
        )
        '''% (month_names),
        (re.VERBOSE | re.IGNORECASE)
        ),
        lambda (m, base_date): datetime(
                base_date.year,
                hashmonths[m.group('month').strip().lower()],
                int(m.group('day') if m.group('day') else 1)
            )
    ),
    (re.compile(
        r'''
        (?P<adverb>%s) # today, yesterday, tomorrow, tonight
        '''% (day_nearest_names),
        (re.VERBOSE | re.IGNORECASE)
        ),
        lambda (m, base_date): dateFromAdverb(base_date, m.group('adverb'))
    ),
    (re.compile(
        r'''
        (?P<named_day>%s) # Mon - Sun
        '''% (day_names),
        (re.VERBOSE | re.IGNORECASE)
        ),
        lambda (m, base_date): this_week_day(
            base_date,
            hashweekdays[m.group('named_day').lower()]
        )
    ),
    (re.compile(
        r'''
        (?P<year>%s) # Year
        '''% (re_year),
        (re.VERBOSE | re.IGNORECASE)
        ),
        lambda (m, base_date): datetime(int(m.group('year')), 1, 1)
    ),
    (re.compile(
        r'''
        (?P<month>%s) # Month
        '''% (month_names),
        (re.VERBOSE | re.IGNORECASE)
        ),
        lambda (m, base_date): datetime(
            base_date.year,
            hashmonths[m.group('month').lower()],
            1
        )
    ),
]

# Hash of numbers
# Append more number to modify your match
def hashnum(number):
    if re.match(r'one|^a\b', number, re.IGNORECASE):
        return 1
    if re.match(r'two', number, re.IGNORECASE):
        return 2
    if re.match(r'three', number, re.IGNORECASE):
        return 3
    if re.match(r'four', number, re.IGNORECASE):
        return 4
    if re.match(r'five', number, re.IGNORECASE):
        return 5
    if re.match(r'six', number, re.IGNORECASE):
        return 6
    if re.match(r'seven', number, re.IGNORECASE):
        return 7
    if re.match(r'eight', number, re.IGNORECASE):
        return 8
    if re.match(r'nine', number, re.IGNORECASE):
        return 9
    if re.match(r'ten', number, re.IGNORECASE):
        return 10
    if re.match(r'eleven', number, re.IGNORECASE):
        return 11
    if re.match(r'twelve', number, re.IGNORECASE):
        return 12
    if re.match(r'thirteen', number, re.IGNORECASE):
        return 13
    if re.match(r'fourteen', number, re.IGNORECASE):
        return 14
    if re.match(r'fifteen', number, re.IGNORECASE):
        return 15
    if re.match(r'sixteen', number, re.IGNORECASE):
        return 16
    if re.match(r'seventeen', number, re.IGNORECASE):
        return 17
    if re.match(r'eighteen', number, re.IGNORECASE):
        return 18
    if re.match(r'nineteen', number, re.IGNORECASE):
        return 19
    if re.match(r'twenty', number, re.IGNORECASE):
        return 20
    if re.match(r'thirty', number, re.IGNORECASE):
        return 30
    if re.match(r'forty', number, re.IGNORECASE):
        return 40
    if re.match(r'fifty', number, re.IGNORECASE):
        return 50
    if re.match(r'sixty', number, re.IGNORECASE):
        return 60
    if re.match(r'seventy', number, re.IGNORECASE):
        return 70
    if re.match(r'eighty', number, re.IGNORECASE):
        return 80
    if re.match(r'ninety', number, re.IGNORECASE):
        return 90
    if re.match(r'hundred', number, re.IGNORECASE):
        return 100
    if re.match(r'thousand', number, re.IGNORECASE):
      return 1000

# Convert strings to numbers
def convert_string_to_number(value):
    if value == None:
        return 1
    if isinstance(value, int):
        return value
    if value.isdigit():
        return int(value)
    num_list = map(lambda s:hashnum(s), re.findall(numbers + '+', value, re.IGNORECASE))
    return sum(num_list)

# Quarter of a year
def dateFromQuarter (base_date, ordinal, year):
    interval = 3
    month_start = interval * (ordinal - 1)
    if month_start < 0:
        month_start = 9
    month_end = month_start + interval
    if month_start == 0:
        month_start = 1
    return [
        datetime(year, month_start, 1),
        datetime(year, month_end, calendar.monthrange(year, month_end)[1])
    ]

# Converts relative day to time
# this tuesday, last tuesday
def dateFromRelativeDay(base_date, time, dow):
    time = time.lower()
    dow = dow.lower()
    if time == 'this':
        # Else day of week
        num = hashweekdays[dow]
        return this_week_day(base_date, num)
    elif time == 'last' or time == 'previous':
        # Else day of week
        num = hashweekdays[dow]
        return previous_week_day(base_date, num)
    elif time == 'next' or time == 'following':
        # Else day of week
        num = hashweekdays[dow]
        return next_week_day(base_date, num)

# Converts relative day to time
# this tuesday, last tuesday
def dateFromRelativeWeekYear(base_date, time, dow):
    if dow in year_variations:
        if time == 'this':
            return datetime(base_date.year, 1, 1)
        elif time == 'last' or time == 'previous':
            return datetime(base_date.year - 1, base_date.month, base_date.day)
    elif dow in week_variations:
        if time == 'this':
            return base_date - timedelta(days=base_date.weekday())
        elif time == 'last' or time == 'previous':
            return base_date - timedelta(weeks=1)

# Convert Day adverbs to dates
# Tomorrow => Date
# Today => Date
def dateFromAdverb(base_date, name):
    if name == 'today' or name == 'tonite' or name == 'tonight':
        return datetime.today()
    elif name == 'yesterday':
        return base_date - timedelta(days=1)
    elif name == 'tomorrow' or name == 'tom':
        return base_date + timedelta(days=1)

# Find dates from duration
# Eg: 20 days from now
# Doesnt support 20 days from last monday
def dateFromDuration(base_date, numberAsString, unit, duration, base_time = None):
    # Check if query is `2 days before yesterday` or `day before yesterday`
    if base_time != None:
        base_date = dateFromAdverb(base_date, base_time)
    num = convert_string_to_number(numberAsString)
    if unit in day_variations:
        args = {'days': num}
    elif unit in minute_variations:
        args = {'minutes': num}
    elif unit in week_variations:
        args = {'weeks': num}
    elif unit in year_variations:
        args = {'years': num}

    if duration == 'ago' or duration == 'before' or duration == 'earlier':
        if ('years' in args):
            return datetime(base_date.year - args['years'], base_date.month, base_date.day)
        return base_date - timedelta(**args)
    elif duration == 'after' or duration == 'later' or duration == 'from now':
        if ('years' in args):
            return datetime(base_date.year + args['years'], base_date.month, base_date.day)
        return base_date + timedelta(**args)

# Finds coming weekday
def this_week_day(base_date, weekday):
    day_of_week = base_date.weekday()
    # If today is Tuesday and the query is `this monday`
    # We should output the next_week monday
    if day_of_week > weekday:
        return next_week_day(base_date, weekday)
    start_of_this_week = base_date - timedelta(days=day_of_week + 1)
    day = start_of_this_week + timedelta(days=1)
    while day.weekday() != weekday:
        day = day + timedelta(days=1)
    return day

# Finds coming weekday
def previous_week_day(base_date, weekday):
    day = base_date.today() - timedelta(days=1)
    while day.weekday() != weekday:
        day = day - timedelta(days=1)
    return day

def next_week_day(base_date, weekday):
    day_of_week = base_date.weekday()
    end_of_this_week = base_date + timedelta(days=6 - day_of_week)
    day = end_of_this_week + timedelta(days=1)
    while day.weekday() != weekday:
        day = day + timedelta(days=1)
    return day


# Mapping of Month name and Value
hashmonths = {
    'january': 1,
    'jan': 1,
    'february': 2,
    'feb': 2,
    'march': 3,
    'mar': 3,
    'april': 4,
    'apr': 4,
    'may': 5,
    'june': 6,
    'jun': 6,
    'july': 7,
    'jul': 7,
    'august': 8,
    'aug': 8,
    'september': 9,
    'sep': 9,
    'october': 10,
    'oct': 10,
    'november': 11,
    'nov': 11,
    'december': 12,
    'dec': 12
}

# Days to number mapping
hashweekdays = {
    'monday': 0,
    'mon': 0,
    'tuesday': 1,
    'tue': 1,
    'wednesday': 2,
    'wed': 2,
    'thursday': 3,
    'thu': 3,
    'friday': 4,
    'fri': 4,
    'saturday': 5,
    'sat': 5,
    'sunday': 6,
    'sun': 6
}

# Ordinal to number
hashordinals = {
    'first': 1,
    'second' : 2,
    'third': 3,
    'fourth': 4,
    'forth': 4,
    'last': -1
}

# Parses date
def datetime_parsing (text, base_date = datetime.now()):
    matches = []
    found_array = []

    # Find the position in the string
    for r, fn in regex:
        for m in r.finditer(text):
            matches.append((m.group(), fn((m, base_date)), m.span()))
        # print (r.pattern)
    # print (text)
    # print (matches)
    # Wrap the matched text with TAG element to prevent nested selections
    for match, value, spans in matches:
        subn = re.subn('(?!<TAG[^>]*?>)' + match + '(?![^<]*?</TAG>)', '<TAG>' + match + '</TAG>', text)
        text = subn[0]
        isSubstituted = subn[1]
        if isSubstituted != 0:
            found_array.append((match, value, spans))

    # To preserve order of the match, sort based on the start position
    return sorted(found_array, key = lambda match: match and match[2][0])
