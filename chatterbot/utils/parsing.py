import re
import calendar
from datetime import timedelta, date, datetime

"""
The first step is the tag the text with <TIMEX>
1. Extract => The meeting is 25 minutes from now => The meeting is <TIMEX>25 minutes from now<TIMEX>
2. Convert to datetime
"""

"""
Regular expression matches
https://github.com/nltk/nltk_contrib/blob/master/nltk_contrib/timex.py
Captured groups
1. Integer + (year|day|week|month|night|minute|min)|unit of duration + duration
2. today|yesterday|tomorrow|tonight
3. this|next|last + year|day|week|month|night|minute|min
4. this|next|last + (monday|tuesday|wednesday|thursday|friday|saturday|sunday)
5. this|next|last + (january|february|march|april|may|june|july|august|september|october|november|december)
6. ISO date
7. Years
8. Day after tomorrow
"""
numbers = "(^a(?=\s)|one|two|three|four|five|six|seven|eight|nine|ten| \
          eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen| \
          eighteen|nineteen|twenty|thirty|forty|fifty|sixty|seventy|eighty| \
          ninety|hundred|thousand)"
day = "(monday|tuesday|wednesday|thursday|friday|saturday|sunday)"
week_day = "(monday|tuesday|wednesday|thursday|friday|saturday|sunday|mon|tue|wed|thu|fri|sat|sun)"
month = "(january|february|march|april|may|june|july|august|september| \
          october|november|december|jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)"
dmy = "(year|day|week|month|night|minute|min)"
rel_day = "(today|yesterday|tomorrow|tonight)"
exp1 = "(before|after|earlier|later|ago|from now)"
exp2 = "(this|next|last)"
iso = "\d+[/-]\d+[/-]\d+ \d+:\d+:\d+\.\d+"
year_exp = "((?<=\s)\d{4}|^\d{4})"
cardinals = "(first|second|third|forth|fourth|last)"
regxp1 = "((\d+|(" + numbers + "[-\s]?)+) " + dmy + "s? " + exp1 + ")"
regxp2 = "(" + exp2 + " (" + dmy + "|" + week_day + "|" + month + "))"
# Matches Sun, 12 January 2012
regxp3 = "(" + day + '[,\s]\s*\d{1,2}' + '\s+' + month + '\s+' + year_exp + ")" 
# Matches 12 January 2012
regxp4 = "(\d{1,2}" + '\s+' + month + '\s' + year_exp + ")"
# Matches day after tomorrow
regxp5 = "(" + dmy + " " + exp1 + " " + rel_day + ")"
# Matches July 3nd
regxp6 = "(" + month + " " + ".*\d{1,2}(st|nd|rd|th)" + "(?:\s*\d{0,4})" + ")"
# First quarter of a year
regxp7=  "(" + cardinals + " quarter of " + year_exp + ")"

reg1 = re.compile(regxp1, re.IGNORECASE)
reg2 = re.compile(regxp2, re.IGNORECASE)
reg3 = re.compile(rel_day, re.IGNORECASE)
reg4 = re.compile(iso)
reg5 = re.compile(year_exp)
reg6 = re.compile(day, re.IGNORECASE)

reg_pattern_3 = re.compile(regxp3, re.IGNORECASE)
reg_pattern_4 = re.compile(regxp4, re.IGNORECASE)
reg_pattern_5 = re.compile(regxp5, re.IGNORECASE)
reg_pattern_6 = re.compile(regxp6, re.IGNORECASE)
reg_pattern_7 = re.compile(regxp7, re.IGNORECASE)

def datetime_parsing(text, base_date = datetime.now()):
    # Initialization
    timex_found = []
    found_array = []

    # reg_pattern_3
    found = reg_pattern_3.findall(text)
    found = [a[0] for a in found if len(a) > 1]
    for timex in found:
        timex_found.append(timex)

    # reg_pattern_4
    found = reg_pattern_4.findall(text)
    found = [a[0] for a in found if len(a) > 1]
    for timex in found:
        timex_found.append(timex)

    # reg_pattern_5
    found = reg_pattern_5.findall(text)
    found = [a[0] for a in found if len(a) > 1]
    for timex in found:
        timex_found.append(timex)

    # reg_pattern_6
    # Check for multiple matches
    found = reg_pattern_6.findall(text)
    found = [a[0] for a in found if len(a) > 1]
    for timex in found:
        timex_found.append(timex)

    # reg_pattern_7
    found = reg_pattern_7.findall(text)
    found = [a[0] for a in found if len(a) > 1]
    for timex in found:
        timex_found.append(timex)

    # re.findall() finds all the substring matches, keep only the full
    # matching string. Captures expressions such as 'number of days' ago, etc.
    found = reg1.findall(text)
    found = [a[0] for a in found if len(a) > 1]
    for timex in found:
        timex_found.append(timex)

    # Variations of this thursday, next year, etc
    found = reg2.findall(text)
    found = [a[0] for a in found if len(a) > 1]
    for timex in found:
        timex_found.append(timex)

    # today, tomorrow, etc
    found = reg3.findall(text)
    for timex in found:
        timex_found.append(timex)

    # ISO
    found = reg4.findall(text)
    for timex in found:
        timex_found.append(timex)

    # Year
    found = reg5.findall(text)
    for timex in found:
        timex_found.append(timex)

    # Day of the week
    found = reg6.findall(text)
    for timex in found:
        timex_found.append(timex)

    # Tag only temporal expressions which haven't been tagged.
    for timex in timex_found:
        text = re.sub(timex + '(?!</TIMEX>)', '<TIMEX>' + timex + '</TIMEX>', text)

    for m in re.finditer('<TIMEX>(.*?)</TIMEX>', text):
        found_array.append((m.group(1), m.span()))

    found_array = ground(found_array, base_date)
    return found_array

# Hash function for week days to simplify the grounding task.
# [Mon..Sun] -> [0..6]
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
    'sun': 6}

# Hash function for months to simplify the grounding task.
# [Jan..Dec] -> [1..12]
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
    'dec': 12}

hashcardinals = {
    'first': 1,
    'second' : 2,
    'third': 3,
    'fourth': 4,
    'forth': 4,
    'last': -1
}

# Hash number in words into the corresponding integer value
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

def next_weekday_by_day(weekday):
    day = date.today() + timedelta(days=1)
    while day.weekday() != weekday:
        day = day + timedelta(days=1)

    return day

def prev_weekday_by_day(weekday):
    day = date.today() - timedelta(days=1)
    while day.weekday() != weekday:
        day = day - timedelta(days=1)

    return day

# Given a timex_tagged_text and a Date object set to base_date,
# returns timex_grounded_text
def ground(found_array, base_date):
    global month
    global week_day
    global hashweekdays
    global hashmonths
    global year_exp

    new_found_array = []
    # Calculate the new date accordingly
    for index, item in enumerate(found_array):
        timex_val = 'UNKNOWN' # Default value
        timex = item[0]
        timex_ori = timex   # Backup original timex for later substitution

        # If numbers are given in words, hash them into corresponding numbers.
        # eg. twenty five days ago --> 25 days ago
        if re.search(numbers, timex, re.IGNORECASE):
            split_timex = re.split(r'\s(?=days?|months?|years?|weeks?|minutes?)', \
                                                              timex, re.IGNORECASE)
            value = split_timex[0]
            unit = split_timex[1]
            num_list = map(lambda s:hashnum(s),re.findall(numbers + '+', \
                                          value, re.IGNORECASE))
            timex = str(sum(num_list)) + ' ' + unit

        # If timex matches ISO format, remove 'time' and reorder 'date'
        if re.match(r'\d+[/-]\d+[/-]\d+ \d+:\d+:\d+\.\d+', timex):
            dmy = re.split(r'\s', timex)[0]
            dmy = re.split(r'/|-', dmy)
            timex_val = str(dmy[2]) + '-' + str(dmy[1]) + '-' + str(dmy[0])

        # Specific dates
        elif re.match(r'\d{4}', timex):
            timex_val = str(timex)

        # Matches Sun, 12 Jan 2010
        elif re.match(r''+ week_day + '[,\s]\s*\d{1,2}' + '\s+' + month + '\s+' + year_exp, timex, re.IGNORECASE):
            matches = re.findall('(.*)[,\s+](\d{1,2})\s(.*)\s(\d{4})', timex)[0]
            timex_val = datetime(int(matches[3]),hashmonths[matches[2].lower()], int(matches[1]))

        # Matches July 2nd
        elif re.match(month + '\s+\d{1,2}(st|nd|rd|th)', timex, re.IGNORECASE):
            matches = re.split(r'\s', timex)
            # Check if year is present
            if matches[2]:
                _year = int(matches[2])
            else:
                _year = base_date.year
            all_dates = []
            all_values = []
            for m in matches:
                if re.match('\d{1,2}(st|nd|rd|th)', m):
                    d = int(re.findall('\d{1,2}', m)[0])
                    all_dates.append(d)
            for d in all_dates:
                all_values.append(datetime(_year, hashmonths[matches[0].lower()], d))
            timex_val = all_values

        # Matches first query
        elif re.match(cardinals + " " + "quarter", timex):
            matches = re.match("(?P<type>" + cardinals + ") " + ".*?" + "(?P<year>" + year_exp + ")", timex)
            interval = 3
            _year = int(matches.group('year'))
            month_start = interval * (int(hashcardinals[matches.group('type')]) - 1)
            if month_start < 0:
                month_start = 9
            # Month end
            month_end = month_start + interval
            if month_start == 0:
                month_start = 1
            timex_val = [
                datetime(int(matches.group('year')), month_start, 1),
                datetime(int(matches.group('year')), month_end, calendar.monthrange(_year, month_end)[1])
            ]

        # Relative dates
        elif re.match(r'tonight|tonite|today', timex, re.IGNORECASE):
            timex_val = base_date
        elif re.match(r'yesterday', timex, re.IGNORECASE):
            timex_val = base_date - timedelta(days=1)
        elif re.match(r'tomorrow', timex, re.IGNORECASE):
            timex_val = base_date + timedelta(days=1)
        elif re.match(r'day after tomorrow', timex, re.IGNORECASE):
            timex_val = base_date + timedelta(days=2)
        elif re.match(r'day before tomorrow', timex, re.IGNORECASE):
            timex_val = base_date - timedelta(days=2)

        # Last night
        elif re.match(r'last night', timex, re.IGNORECASE):
            timex_val = base_date - timedelta(days=1)
        # Weekday in the previous week.
        elif re.match(r'last ' + week_day, timex, re.IGNORECASE):
            _day = hashweekdays[timex.split()[1].lower()]
            timex_val = prev_weekday_by_day(_day)

        # Weekday in the current week.
        elif re.match(r'this ' + week_day, timex, re.IGNORECASE):
            _day = hashweekdays[timex.split()[1].lower()]
            timex_val = next_weekday_by_day(_day)

        # Weekday in the following week.
        elif re.match(r'next ' + week_day, timex, re.IGNORECASE):
            _day = hashweekdays[timex.split()[1].lower()]
            timex_val = next_weekday_by_day(_day)

        # Last, this, next week.
        elif re.match(r'last week', timex, re.IGNORECASE):
            timex_val = base_date - timedelta(weeks=1)
        elif re.match(r'this week', timex, re.IGNORECASE):
            timex_val = base_date - timedelta(days=base_date.weekday())
        elif re.match(r'next week', timex, re.IGNORECASE):
            timex_val = base_date + timedelta(weeks=1)

        # Month in the previous year.
        elif re.match(r'last ' + month, timex, re.IGNORECASE):
            month = hashmonths[timex.split()[1].lower()]
            timex_val = datetime(base_date.year - 1, month)

        # Month in the current year.
        elif re.match(r'this ' + month, timex, re.IGNORECASE):
            month = hashmonths[timex.split()[1].lower()]
            timex_val = datetime(base_date.year, month)

        # Month in the following year.
        elif re.match(r'next ' + month, timex, re.IGNORECASE):
            month = hashmonths[timex.split()[1]]
            timex_val = datetime(base_date.year + 1, month)
        elif re.match(r'last month', timex, re.IGNORECASE):

            # Handles the year boundary.
            if base_date.month == 1:
                timex_val = datetime(base_date.year - 1, 12)
            else:
                timex_val = datetime(base_date.year, base_date.month - 1)
        elif re.match(r'this month', timex, re.IGNORECASE):
                timex_val = datetime(base_date.year, base_date.month)
        elif re.match(r'next month', timex, re.IGNORECASE):
            # Handles the year boundary.
            if base_date.month == 12:
                timex_val = datetime(base_date.year + 1, 1, 1)
            else:
                timex_val = datetime(base_date.year, base_date.month + 1, 1)
        elif re.match(r'last year', timex, re.IGNORECASE):
            timex_val = datetime(base_date.year - 1)
        elif re.match(r'this year', timex, re.IGNORECASE):
            timex_val = datetime(base_date.year)
        elif re.match(r'next year', timex, re.IGNORECASE):
            timex_val = datetime(base_date.year + 1)
        # Minutes past/future
        elif re.match(r'\d+ minutes? (ago|earlier|before)', timex, re.IGNORECASE):
            offset = int(re.split(r'\s', timex)[0])
            timex_val = base_date - timedelta(minutes=offset)
        elif re.match(r'\d+ minutes? (later|after|from now)', timex, re.IGNORECASE):
            offset = int(re.split(r'\s', timex)[0])
            d = datetime.now() + timedelta(minutes=offset)
            timex_val = base_date + timedelta(minutes=offset)
        elif re.match(r'\d+ mins? (ago|earlier|before)', timex, re.IGNORECASE):
            offset = int(re.split(r'\s', timex)[0])
            timex_val = base_date - timedelta(minutes=offset)
        elif re.match(r'\d+ mins? (later|after|from now)', timex, re.IGNORECASE):
            offset = int(re.split(r'\s', timex)[0])
            timex_val = base_date - timedelta(minutes=offset)
        # Days past/future
        elif re.match(r'\d+ days? (ago|earlier|before)', timex, re.IGNORECASE):
            # Calculate the offset by taking '\d+' part from the timex.
            offset = int(re.split(r'\s', timex)[0])
            timex_val = base_date - timedelta(days=offset)
        elif re.match(r'\d+ days? (later|after|from now)', timex, re.IGNORECASE):
            offset = int(re.split(r'\s', timex)[0])
            timex_val = base_date + timedelta(days=offset)
        elif re.match(r'\d+ weeks? (ago|earlier|before)', timex, re.IGNORECASE):
            offset = int(re.split(r'\s', timex)[0])
            timex_val = base_date - timedelta(weeks=offset)
        elif re.match(r'\d+ weeks? (later|after)', timex, re.IGNORECASE):
            offset = int(re.split(r'\s', timex)[0])
            timex_val = base_date + timedelta(weeks=offset)
        elif re.match(r'\d+ months? (ago|earlier|before)', timex, re.IGNORECASE):
            extra = 0
            offset = int(re.split(r'\s', timex)[0])

            # Checks if subtracting the remainder of (offset / 12) to the base month
            # crosses the year boundary.
            if (base_date.month - offset % 12) < 1:
                extra = 1

            # Calculate new values for the year and the month.
            year = int(base_date.year - offset // 12 - extra)
            month = int((base_date.month - offset % 12) % 12)

            # Fix for the special case.
            if month == 0:
                month = 12
            timex_val = datetime(year, month)
        elif re.match(r'\d+ months? (later|after)', timex, re.IGNORECASE):
            extra = 0
            offset = int(re.split(r'\s', timex)[0])
            if (base_date.month + offset % 12) > 12:
                extra = 1
            year = int(base_date.year + offset // 12 + extra)
            month = int((base_date.month + offset % 12) % 12)
            if month == 0:
                month = 12
            timex_val = datetime(year, month)
        elif re.match(r'\d+ years? (ago|earlier|before)', timex, re.IGNORECASE):
            offset = int(re.split(r'\s', timex)[0])
            timex_val = datetime(base_date.year - offset)
        elif re.match(r'\d+ years? (later|after)', timex, re.IGNORECASE):
            offset = int(re.split(r'\s', timex)[0])
            timex_val = datetime(base_date.year + offset)

        # Days only
        elif re.match(day, timex, re.IGNORECASE):
            timex_val = datetime(base_date.year, base_date.month, hashweekdays[timex.strip().lower()])

        if timex_val != 'UNKNOWN':
            new_found_array.append((timex_val, item[1]))
    return new_found_array