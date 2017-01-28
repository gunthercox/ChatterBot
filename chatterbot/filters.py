"""
Filters set the base query that gets passed to the storage adapter.
"""


class Filter(object):
    """
    A base filter object from which all other
    filters should be subclassed.
    """

    def filter_selection(self, chatterbot, conversation_id):
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

    def filter_selection(self, chatterbot, conversation_id):

        conversation = chatterbot.conversations.get(conversation_id)

        # Check if a conversation of some length exists
        if not conversation.statements.exists():
            return chatterbot.storage.base_query

        text_of_recent_responses = []

        skip = True

        for statement in conversation.statements.all():

            # Skip every other statement to only filter out the bot's responses
            if skip:
                skip = False
            else:
                skip = True
                text_of_recent_responses.append(statement.text)

        query = chatterbot.storage.base_query.statement_text_not_in(
            text_of_recent_responses
        )

        return query
