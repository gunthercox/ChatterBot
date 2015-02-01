def get_closest_statement(text, log_directory):
    """
    Takes a statement from a conversation.
    Returns a the closest matching statement in the database.
    """
    import os
    from jsondb.db import Database
    from fuzzywuzzy import fuzz
    import random

    closest_statement = None
    closest_ratio = 0

    database = Database(log_directory)
    data = database.data()

    # Return immediately if an exact match exists
    if text in data:
        return {text: data[text]}

    for statement in data:
        ratio = fuzz.ratio(statement, text)

        if ratio > closest_ratio:
            closest_ratio = ratio
            closest_statement = statement

        # If the ratios are the same, pick the one to keep at random
        elif ratio == closest_ratio and closest_ratio != 0:

            # Use a random boolean to determine which statement to keep
            if bool(random.getrandbits(1)):
                closest_statement = statement

    return {closest_statement: data[closest_statement]}

def engram(text, log_directory):
    """
    Returns the statement after the closest matchng statement in
    the conversation.
    """
    import os
    from jsondb.db import Database
    import random

    matching_responces = []
    database = Database(log_directory).data()

    # If no text was passed in, then return a random statement.
    if not text or not text.strip():
        selection = random.choice(list(database.keys()))
        return {selection: database[selection]}

    closest_statement = get_closest_statement(text, log_directory)
    closest_statement_key = list(closest_statement.keys())[0]

    for statement in database:

        if "in_response_to" in database[statement]:
            in_response_to = database[statement]["in_response_to"]

            # check if our closest statement is in this list
            if closest_statement_key in in_response_to:
                matching_responces.append(statement)

    # If no matching responses are found: return something random
    if not matching_responces:
        selection = random.choice(list(database.keys()))
        return {selection: database[selection]}

    # Choose from the selection of matching responces
    selection = random.choice(matching_responces)
    return {selection: database[selection]} 
