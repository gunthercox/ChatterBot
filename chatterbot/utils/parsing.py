import re
from datetime import timedelta, date, datetime
import calendar

day_names = 'monday|tuesday|wednesday|thursday|friday|saturday|sunday'
month_names = 'january|february|march|april|may|june|july|august|september|october|november|december|jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec'
day_nearest_names = 'today|yesterday|tomorrow|tonight'
numbers = "(^a(?=\s)|one|two|three|four|five|six|seven|eight|nine|ten| \
                    eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen| \
                    eighteen|nineteen|twenty|thirty|forty|fifty|sixty|seventy|eighty| \
                    ninety|hundred|thousand)"
re_dmy = '(year|day|week|month|night|minute|min)'
re_duration = '(before|after|earlier|later|ago|from now)'
re_year = "((?<=\s)\d{4}|^\d{4})"

regex = [
    (re.compile(
        r'''
        (
            (%s) # day_names
            [,\s]\s*\d{1,2} # Any digit
            \s+ # One or more space
            (%s) # Month names
            \s+ # One or more space
            %s # Year
        )
        '''% (day_names, month_names, re_year),
        (re.VERBOSE | re.IGNORECASE)
        ),
        lambda m: datetime.today()
    ),
    (re.compile(
        r'''
        (
            \d{1,2}
            \s+
            %s
            \s
            %s # Year
        )
        '''% (month_names, re_year),
        (re.VERBOSE | re.IGNORECASE)
        ),
    lambda m: datetime.today()
    ),
    (re.compile(
        r'''
        (
            (?P<number>\d+|(%s[-\s]?)+)\s
            (?P<unit>%ss?\s)
            (?P<duration>%s)
        )
        '''% (numbers, re_dmy, re_duration),
        (re.VERBOSE | re.IGNORECASE)
        ),
        lambda m: m.group('number') + m.group('unit') + m.group('duration')
    ),
    (re.compile(
        r'''
        (%s)
        '''% (day_nearest_names),
        (re.VERBOSE | re.IGNORECASE)
        ),
        lambda m: datetime.today()
    ),
    (re.compile(
        r'''
        (%s)
        '''% day_names,
        (re.VERBOSE | re.IGNORECASE),
        ),
        lambda m: datetime.today()
    )
]

# Parses date
def datetime_parsing (text):
    matches = []
    found_array = []
    resolved_array = []
    original_text = text

    # Find the position in the string
    for r, fn in regex:
        for m in r.finditer(text):
            matches.append((m.group(), fn(m), m.span()))

    # We need to wrap the matched text with TAG element to prevent nested selections
    for match, value, spans in matches:
        subn = re.subn('(?!<TAG[^>]*?>)' + match + '(?![^<]*?</TAG>)', '<TAG>' + match + '</TAG>', text)
        text = subn[0]
        isSubstituted = subn[1]
        if isSubstituted != 0:
            found_array.append((match, value, spans))

    return found_array
