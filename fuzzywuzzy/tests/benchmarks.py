# -*- coding: utf8 -*-

from timeit import timeit
import math

iterations = 100000

cirque_strings = [
    "cirque du soleil - zarkana - las vegas",
    "cirque du soleil ",
    "cirque du soleil las vegas",
    "zarkana las vegas",
    "las vegas cirque du soleil at the bellagio",
    "zarakana - cirque du soleil - bellagio"
]

choices = [
    "",
    "new york yankees vs boston red sox",
    "",
    "zarakana - cirque du soleil - bellagio",
    None,
    "cirque du soleil las vegas",
    None
]

mixed_strings = [
    "Lorem Ipsum is simply dummy text of the printing and typesetting industry.",
    "C\\'est la vie",
    u"Ça va?",
    u"Cães danados",
    u"\xacCamarões assados",
    u"a\xac\u1234\u20ac\U00008000"
]

common_setup = "from fuzzywuzzy import fuzz, utils; "
basic_setup = "from fuzzywuzzy.string_processing import StringProcessor;"


def print_result_from_timeit(stmt='pass', setup='pass', number=1000000):
    """
    Clean function to know how much time took the execution of one statement
    """
    units = ["s", "ms", "us", "ns"]
    duration = timeit(stmt, setup, number=number)
    avg_duration = duration / float(number)
    thousands = int(math.floor(math.log(avg_duration, 1000)))

    print "Total time: %fs. Average run: %.3f%s." \
        % (duration, avg_duration * (1000 ** -thousands), units[-thousands])

for s in choices:
    print 'Test validate_string for: "%s"' % s
    print_result_from_timeit('utils.validate_string(\'%s\')' % s, common_setup, number=iterations)

print

for s in mixed_strings + cirque_strings + choices:
    print 'Test full_process for: "%s"' % s
    print_result_from_timeit('utils.full_process(u\'%s\')' % s,
                             common_setup + basic_setup, number=iterations)

### benchmarking the core matching methods...

for s in cirque_strings:
    print 'Test fuzz.ratio for string: "%s"' % s
    print '-------------------------------'
    print_result_from_timeit('fuzz.ratio(u\'cirque du soleil\', u\'%s\')' % s,
                             common_setup + basic_setup, number=iterations / 100)

for s in cirque_strings:
    print 'Test fuzz.partial_ratio for string: "%s"' % s
    print '-------------------------------'
    print_result_from_timeit('fuzz.partial_ratio(u\'cirque du soleil\', u\'%s\')'
                             % s, common_setup + basic_setup, number=iterations / 100)

for s in cirque_strings:
    print 'Test fuzz.WRatio for string: "%s"' % s
    print '-------------------------------'
    print_result_from_timeit('fuzz.WRatio(u\'cirque du soleil\', u\'%s\')' % s,
                             common_setup + basic_setup, number=iterations / 100)
