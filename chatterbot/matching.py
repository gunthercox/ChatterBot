'''
A collection of methods used to find the closest known match
to an existing statement in the database.
'''

def closest(text, database):
    """
    Takes a statement from the current conversation and a database instance.
    Returns a the closest known statement that matches by string comparison.
    """
    from fuzzywuzzy import process

    # Check if an exact match exists
    if text in database:
        return text

    # Get the closest matching statement from the database
    return process.extract(text, database[0].keys(), limit=1)[0][0]

def similar(text, database):
    """
    Returns the closest known statement based on the meaning of the statement.
    """
    # TODO
    pass
