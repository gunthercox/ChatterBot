from chatterbot.algorithms.matching import closest


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

    closest_statement = closest(text, log_directory)
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
