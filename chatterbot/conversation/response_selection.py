import logging

"""
Response selection methods determines which response should be used in
the event that multiple responses are generated within a logic adapter.
"""

def get_most_frequent_response(input_statement, response_list):
    """
    Returns the statement with the greatest number of occurrences.
    """
    matching_response = None
    occurrence_count = -1

    logger = logging.getLogger(__name__)
    logger.info(u'Selecting response with greatest number of occurrences.')

    for statement in response_list:
        count = statement.get_response_count(input_statement)

        # Keep the more common statement
        if count >= occurrence_count:
            matching_response = statement
            occurrence_count = count

    # Choose the most commonly occuring matching response
    return matching_response

def get_first_response(input_statement, response_list):
    """
    Return the first statement in the response list.
    """
    logger = logging.getLogger(__name__)
    logger.info(u'Selecting first response from list of {} options.'.format(
        len(response_list)
    ))
    return response_list[0]

def get_random_response(input_statement, response_list):
    """
    Choose a random response from the selection.
    """
    from random import choice
    logger = logging.getLogger(__name__)
    logger.info(u'Selecting a response from list of {} options.'.format(
        len(response_list)
    ))
    return choice(response_list)
