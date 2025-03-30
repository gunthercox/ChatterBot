"""
Statement pre-processors.
"""
from chatterbot.conversation import Statement
from unicodedata import normalize
from re import sub as re_sub
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
