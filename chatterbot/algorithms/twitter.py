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

def twitter(text, consumer_key, consumer_secret):
    from chatterbot.conversation import Statement
    from chatterbot.apis.twitter import Twitter
    from chatterbot.apis import clean
    import random

    api = TwitterAPI(consumer_key, consumer_secret)
    results = api.get_related_messages(text)

    output = []
    for result in results:

        # Clean the text
        result = clean(result)

        # Remove leeding usernames
        result = remove_leeding_usernames(text)

        # Remove trailing usernames
        result = remove_trailing_usernames(text)

        # Ignore single usernames
        if len(result.split()) > 0 and result[0] != "@":
            output.append(result)

    # Pick a random statement as the default
    closest_statement = random.choice(output)
    closest_value = 0

    # The sentence with the most words is typically a good response
    longest_statement = random.choice(output)
    longest_value = len(longest_statement.split())

    for statement in output:
        value = 0
        if len(statement.split()) > longest_value:
            longest_value = value
            longest_statement = statement

    # Find the statement that has the closest matching number of words
    words = text.lower().split()
    for statement in output:
        value = 0
        for word in statement.lower().split():
            if word in words:
                value += 1

        if value > closest_value:
            closest_value = value
            closest_statement = statement

    # If results were found
    if len(output) > 0:
        return [Statement("Twitter", closest_statement)]
    else:
        return [Statement("Error", "Twitter is a poor source of knowledge at the moment.")]
