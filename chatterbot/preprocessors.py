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
    import html

    statement.text = html.unescape(statement.text)

    return statement


def convert_to_ascii(chatbot, statement):
    """
    Converts unicode characters to ASCII character equivalents.
    For example: "på fédéral" becomes "pa federal".
    """
    import unicodedata

    text = unicodedata.normalize('NFKD', statement.text)
    text = text.encode('ascii', 'ignore').decode('utf-8')

    statement.text = str(text)
    return statement

def tweet_clean(chatbot, statement):
    """
    Strips links, # from hashtags and mentions
    """
    import re
    
    text = re.sub('http\S+\s*', '', text)  # remove URLs
    text = re.sub('RT|cc', '', text)  # remove 'RT' and 'cc'
    text = re.sub('#', '', text)  # remove # from hashtags
    text = re.sub('@\S+', '', text)  # remove mentions
    text = re.sub('\s+', ' ', text)  # remove extra whitespace
    statement.text = str(text)
    return statement
