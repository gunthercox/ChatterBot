# -*- coding: utf-8 -*-
"""
Statement pre-processors.
"""


def clean_whitespace(chatbot, statement):
    """
    Remove any consecutive whitespace characters from the statement text.
    """
    import re

    # Replace linebreaks and tabs with spaces
    statement.text = statement.text.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')

    # Remove any leeding or trailing whitespace
    statement.text = statement.text.strip()

    # Remove consecutive spaces
    statement.text = re.sub(' +', ' ', statement.text)

    return statement


def unescape_html(chatbot, statement):
    """
    Convert escaped html characters into unescaped html characters.
    For example: "&lt;b&gt;" becomes "<b>".
    """
    import sys

    # Replace HTML escape characters
    if sys.version_info[0] < 3:
        from HTMLParser import HTMLParser
        html = HTMLParser()
    else:
        import html

    statement.text = html.unescape(statement.text)

    return statement


def convert_to_ascii(chatbot, statement):
    """
    Converts unicode characters to ASCII character equivalents.
    For example: "på fédéral" becomes "pa federal".
    """
    import unicodedata
    import sys

    # Normalize unicode characters
    if sys.version_info[0] < 3:
        statement.text = unicode(statement.text) # NOQA

    text = unicodedata.normalize('NFKD', statement.text)
    text = text.encode('ascii', 'ignore').decode('utf-8')

    statement.text = str(text)
    return statement
