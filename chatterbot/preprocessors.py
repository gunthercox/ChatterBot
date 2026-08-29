"""
Statement pre-processors.
"""
from chatterbot.conversation import Statement
from unicodedata import normalize
from re import sub as re_sub, compile as re_compile
from html import unescape


def clean_whitespace(statement: Statement) -> Statement:
    """
    Remove any consecutive whitespace characters from the statement text.
    """
    # Replace linebreaks and tabs with spaces
    # Uses splitlines() which includes a superset of universal newlines:
    # https://docs.python.org/3/library/stdtypes.html#str.splitlines
    statement.text = ' '.join(statement.text.splitlines()).replace('\t', ' ')

    # Remove any leading or trailing whitespace
    statement.text = statement.text.strip()

    # Remove consecutive spaces
    statement.text = re_sub(' +', ' ', statement.text)

    return statement


def unescape_html(statement: Statement) -> Statement:
    """
    Convert escaped html characters into unescaped html characters.
    For example: "&lt;b&gt;" becomes "<b>".
    """
    statement.text = unescape(statement.text)

    return statement


def convert_to_ascii(statement: Statement) -> Statement:
    """
    Converts unicode characters to ASCII character equivalents.
    For example: "på fédéral" becomes "pa federal".
    """
    text = normalize('NFKD', statement.text)
    text = text.encode('ascii', 'ignore').decode('utf-8')

    statement.text = str(text)
    return statement

# Matches a single letter that is immediately repeated three or more times.
# Digits, punctuation, and whitespace are intentionally excluded so that
# values such as "1000000" or "!!!" are left unchanged.
_REPEATING_CHARACTER_PATTERN = re_compile(r'([^\W\d_])\1{2,}')


def normalize_repeating_characters(statement: Statement) -> Statement:
    """
    Reduce runs of three or more repeated letters down to two.

    Elongated words are common in conversational text (for example
    "I am sooooo happy"). Collapsing the repeated characters maps these
    variations to a single, consistent form ("I am soo happy") which helps
    the chat bot match input against statements it has been trained on.

    Letter pairs that occur naturally (such as the "oo" in "cool") are
    preserved, and repeated digits or punctuation are left unchanged.
    """
    statement.text = _REPEATING_CHARACTER_PATTERN.sub(
        lambda match: match.group(1) * 2, statement.text
    )

    return statement
