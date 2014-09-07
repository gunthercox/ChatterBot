from __future__ import unicode_literals
import re


class StringProcessor(object):
    """
    This class defines method to process strings in the most
    efficient way. Ideally all the methods below use unicode strings
    for both input and output.
    """

    @classmethod
    def replace_non_letters_non_numbers_with_whitespace(cls, a_string):
        """
        This function replaces any sequence of non letters and non
        numbers with a single white space.
        """
        #regex = re.compile(r"(?ui)\W")
        #return regex.sub(" ", a_string)
        return ''.join([i if ord(i) < 128 else ' ' for i in a_string])

    @classmethod
    def strip(cls, a_string):
        """
        This function strips leading and trailing white space.
        """

        return a_string.strip()

    @classmethod
    def to_lower_case(cls, a_string):
        """
        This function returns the lower-cased version of the string given.
        """
        return a_string.lower()

    @classmethod
    def to_upper_case(cls, a_string):
        """
        This function returns the upper-cased version of the string given.
        """
        return a_string.upper()
