from chatterbot.algorithms.matching import closest


def engram(text, log_directory):
    """
    Returns the statement after the closest matchng statement in
    the conversation.
    """
    import os
    from jsondb.db import Database
    import random

    database = Database(log_directory)

    # Initialize the matching responce with a random statement from the database
    matching_responces = random.choice(list(database))
    occurrence_count = database[matching_responces]["occurrence"]

    closest_statement = closest(text, log_directory)

    for statement in database:

        if "in_response_to" in database[statement]:

            # Check if our closest statement is in this list
            if closest_statement in database[statement]["in_response_to"]:

                # Keep the more common statement
                if database[statement]["occurrence"] >= occurrence_count:
                    matching_responces = statement
                    occurrence_count = database[statement]["occurrence"]

                # If the two statements occure equaly in frequency, keep one at random

    # Choose the most common selection of matching responces
    return {matching_responces: database[matching_responces]}
