def clean(text):
    """
    A function for cleaning a string of text.
    Returns valid ASCII characters.
    """
    import re, unicodedata

    # Replace linebreaks with spaces
    text = text.replace("\n", " ").replace("\r", " ").replace("\t", " ")

    # Remove any leeding or trailing whitespace
    text = text.strip()

    # Remove consecutive spaces
    text = re.sub(" +", " ", text)

    # Remove links from message
    #text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)

    # Replace html characters with ascii equivilant
    text = text.replace("&amp;", "&")
    text = text.replace("&gt;", ">")
    text = text.replace("&lt;", "<")
    text = text.replace("&#039;", "'")
    text = text.replace("&quot;", "\"")
    text = text.replace("&#064;", "@")

    # Normalize unicode characters
    text = unicodedata.normalize('NFKD', text).encode('ascii','ignore').decode("utf-8")

    return text
