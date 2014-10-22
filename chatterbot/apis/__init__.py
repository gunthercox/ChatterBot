def clean(text):
    """
    A function for cleaning a string of text.
    Returns valid ASCII characters.
    """
    import re, json, string
    import unicodedata

    # Remove links from message
    text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)

    # Replace linebreaks with spaces
    text = text.replace("\n", " ").replace("\r", " ").replace("\t", " ")

    # Remove any leeding or trailing whitespace
    text = text.strip()

    # Normalize unicode characters
    text = str(unicodedata.normalize('NFKD', text).encode('ascii','ignore'))

    # Remove non-ascii characters
    text = filter(lambda x: x in string.printable, text)

    # Replace html characters with ascii equivilant
    text = text.replace("&amp;", "&")
    text = text.replace("&gt;", ">")
    text = text.replace("&lt;", "<")

    # Remove leeding usernames
    if (len(text) > 0) and (len(text.split(" ",1)) > 0) and (text[0] == "@"):
        text = text.split(" ",1)[1]
        text = clean(text)

    # Remove trailing usernames
    if (len(list(text.split(" ")[-1])) > 0) and (list(text.split(" ")[-1])[0] == "@"):
        text = text.rsplit(" ", 1)[0]

    return text
