"""
Filters set the base query that gets passed to the storage adapter.
"""


class Filter(object):
    """
    A base filter object from which all other
    filters should be subclassed.
    """

    def filter_selection(self, chatterbot, session_id):
        """
        Because this is the base filter class, this method just
        returns the storage adapter's base query. Other filters
        are expected to override this method.
        """
        return chatterbot.storage.base_query


class RepetitiveResponseFilter(Filter):
    """
    A filter that eliminates possibly repetitive responses to prevent
    a chat bot from repeating statements that it has recently said.
    """

    def filter_selection(self, chatterbot, session_id):

        session = chatterbot.conversation_sessions.get(session_id)

        if session.conversation.empty():
            return chatterbot.storage.base_query

        text_of_recent_responses = []

        for statement, response in session.conversation:
            text_of_recent_responses.append(response.text)

        query = chatterbot.storage.base_query.statement_text_not_in(
            text_of_recent_responses
        )

        return query
