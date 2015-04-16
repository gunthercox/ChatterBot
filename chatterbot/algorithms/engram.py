def get_occurrence_count(key, database):
    # TODO: Move this into a database adaptor class

    if "occurrence" in database[key]:
        return database[key]["occurrence"]

    # If the number of occurances has not been set then return 1
    return 1

# TODO:
# Change engram into a class and make classes for getting statements into
# methods that can be easially tested
def engram(closest_statement, database):
    """
    Returns a statement in response to the closest matching statement in
    the database. For each match, the statement with the greatest number
    of occurrence will be returned.
    """

    if not closest_statement in database:
        raise Exception("A matching statement must exist in the database")

    # Initialize the matching responce with the first statement in the database
    # The list of keys has to be cast as a list for python 3
    matching_response = list(database[0].keys())[0]
    occurrence_count = get_occurrence_count(matching_response, database)

    for statement in database:

        if "in_response_to" in database[statement]:

            # Check if our closest statement is in this list
            if closest_statement in database[statement]["in_response_to"]:

                statement_occurrence_count = get_occurrence_count(statement, database)

                # Keep the more common statement
                if statement_occurrence_count >= occurrence_count:
                    matching_response = statement
                    occurrence_count = statement_occurrence_count

                #TODO? If the two statements occure equaly in frequency, should we keep one at random

    # Choose the most common selection of matching response
    return {matching_response: database[matching_response]}
