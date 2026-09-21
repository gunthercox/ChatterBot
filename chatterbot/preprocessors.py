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
# No correctly spelled English word contains a run of that length, so a run
# of three or more is always an intentional elongation and can be reduced
# without altering text that was already spelled correctly. Digits,
# punctuation, and whitespace are excluded from the pattern so that values
# such as "1000000" or "!!!" are left unchanged.
_REPEATING_CHARACTER_PATTERN = re_compile(r'([^\W\d_])\1{2,}')


def normalize_repeating_characters(statement: Statement) -> Statement:
    """
    Reduce runs of three or more repeated letters down to a single letter.

    Elongated words are common in conversational text (for example
    "I am sooooo happy"). Reducing the repeated characters maps these
    variations onto the word being elongated ("I am so happy") which helps
    the chat bot match input against statements it has been trained on.

    Only runs of three or more characters are reduced, so letter pairs that
    occur naturally (such as the "oo" in "cool") are left untouched, as are
    repeated digits and punctuation ("1000000" and "!!!").

    Note that a word which genuinely contains a doubled letter is reduced
    past its correct spelling when it is elongated, so "gooood" becomes
    "god" rather than "good". Distinguishing the two cases requires a
    dictionary lookup, which is intentionally outside the scope of a
    preprocessor; a project that needs that distinction can register its own
    preprocessor with access to a word list.
    """
    statement.text = _REPEATING_CHARACTER_PATTERN.sub(r'\1', statement.text)

    return statement
