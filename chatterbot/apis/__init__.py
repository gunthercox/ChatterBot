def remove_leeding_usernames(text):

    # The base case is that the is only one word
    if not len(text.split(" ", 1)) > 1:
        return text

    if text and text[0] == "@":
        if len(text.split(" ", 1)) > 1:

            # Split the text at the first space character
            text = text.split(" ", 1)[1]
            text = "".join(text)

    if text and text[0] == "@":
        text = remove_leeding_usernames(text)

    return text

def remove_trailing_usernames(text):

    # The base case is that the is only one word
    if not len(text.split(" ", 1)) > 1:
        return text

    last_word = text.split(" ")[-1]

    if len(last_word) > 0 and last_word[0] == "@":
        text = text[:-len(last_word)]
        text = text.strip()

    last_word = text.split(" ")[-1]

    if last_word[0] == "@":
        text = remove_trailing_usernames(text)

    return text

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

    # Remove leeding usernames
    text = remove_leeding_usernames(text)

    # Remove trailing usernames
    text = remove_trailing_usernames(text)

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
