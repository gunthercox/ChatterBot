# Filters set the base query that gets passed to the storage adapter


class Filter(object):
    """
    A base filter object from which all other
    filters should be subclassed.
    """

    def filter_selection(self, chatterbot):
        return chatterbot.storage.base_query


class RepetitiveResponseFilter(Filter):
    """
    A filter that eliminates possibly repetitive
    responses to prevent a chat bot from repeating
    statements that it has recently said.
    """

    def filter_selection(self, chatterbot):

        if chatterbot.recent_statements.empty():
            return chatterbot.storage.base_query

        text_of_recent_responses = []

        for statement, response in chatterbot.recent_statements:
            text_of_recent_responses.append(response.text)

        query = chatterbot.storage.base_query.statement_text_not_in(
            text_of_recent_responses
        )

        return query

