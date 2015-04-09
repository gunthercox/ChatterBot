def engram(closest_statement, database):
    """
    Returns a statement in response to the closest matching statement in
    the database. For each match, the statement with the greatest number
    of occurrence will be returned.
    """

    if not closest_statement in database:
        raise Exception("A matching statement must exist in the database")

    # Initialize the matching responce with the first statement in the database
    matching_response = database[0].keys()[0]
    occurrence_count = database[matching_response]["occurrence"]

    for statement in database:

        if "in_response_to" in database[statement]:

            # Check if our closest statement is in this list
            if closest_statement in database[statement]["in_response_to"]:

                # Keep the more common statement
                if database[statement]["occurrence"] >= occurrence_count:
                    matching_response = statement
                    occurrence_count = database[statement]["occurrence"]

                #TODO? If the two statements occure equaly in frequency, should we keep one at random

    # Choose the most common selection of matching response
    return {matching_response: database[matching_response]}
