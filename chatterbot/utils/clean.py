import re


def clean_whitespace(text):
    """
    Remove any extra whitespace and line breaks as needed.
    """
    # Replace linebreaks with spaces
    text = text.replace("\n", " ").replace("\r", " ").replace("\t", " ")

    # Remove any leeding or trailing whitespace
    text = text.strip()

    # Remove consecutive spaces
    text = re.sub(" +", " ", text)

    return text


def clean(text):
    """
    A function for cleaning a string of text.
    Returns valid ASCII characters.
    """
    import unicodedata
    import sys

    text = clean_whitespace(text)

    # Remove links from message
    # text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)

    # Replace HTML escape characters
    if sys.version_info[0] < 3:
        from HTMLParser import HTMLParser
        parser = HTMLParser()
        text = parser.unescape(text)
    else:
        import html.parser
        parser = html.parser.HTMLParser()
        text = parser.unescape(text)

    # Normalize unicode characters
    # 'raw_input' is just 'input' in python3
    if sys.version_info[0] < 3:
        text = unicode(text)
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("utf-8")

    return str(text)
