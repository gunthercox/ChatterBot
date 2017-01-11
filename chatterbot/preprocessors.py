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
    For example: &lt;b&gt; becomes <b>
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
