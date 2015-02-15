def closest(text, log_directory):
    """
    Takes a statement from a conversation.
    Returns a the closest matching statement in the database.
    """
    import os
    from jsondb.db import Database
    from fuzzywuzzy import fuzz
    from stemming.porter2 import stem
    import random


    database = Database(log_directory)


    # Initialize the closest statement to a random item in the database
    closest_statement = random.choice(database)
    closest_ratio = 0

    # Return immediately if an exact match exists
    if text in database:
        return text

    for statement in database:

        stemmed_statement = stem(statement)
        stemmed_text = stem(text)

        # Get the difference ratio of the stemmed statements
        ratio = fuzz.ratio(stemmed_statement, stemmed_text)

        if ratio > closest_ratio:
            closest_ratio = ratio
            closest_statement = statement

        # Keep one statement at random if the ratios are the same
        elif ratio == closest_ratio:

            # Use a random boolean to determine which statement to keep
            if bool(random.getrandbits(1)):
                closest_statement = statement

    return closest_statement
