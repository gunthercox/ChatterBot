"""
Response selection methods determines which response should be used in
the event that multiple responses are generated within a logic adapter.
"""
import logging


def get_most_frequent_response(input_statement, response_list):
    """
    :param input_statement: A statement, that closely matches an input to the chat bot.
    :type input_statement: Statement

    :param response_list: A list of statement options to choose a response from.
    :type response_list: list

    :return: The response statement with the greatest number of occurrences.
    :rtype: Statement
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
    :param input_statement: A statement, that closely matches an input to the chat bot.
    :type input_statement: Statement

    :param response_list: A list of statement options to choose a response from.
    :type response_list: list

    :return: Return the first statement in the response list.
    :rtype: Statement
    """
    logger = logging.getLogger(__name__)
    logger.info(u'Selecting first response from list of {} options.'.format(
        len(response_list)
    ))
    return response_list[0]


def get_random_response(input_statement, response_list):
    """
    :param input_statement: A statement, that closely matches an input to the chat bot.
    :type input_statement: Statement

    :param response_list: A list of statement options to choose a response from.
    :type response_list: list

    :return: Choose a random response from the selection.
    :rtype: Statement
    """
    from random import choice
    logger = logging.getLogger(__name__)
    logger.info(u'Selecting a response from list of {} options.'.format(
        len(response_list)
    ))
    return choice(response_list)
