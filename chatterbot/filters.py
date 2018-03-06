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

        responses = chatterbot.storage.get_statements_for_conversation(
            conversation_id
        )

        text_of_recent_responses = set()
        text_of_all_responses = []

        for response in responses:

            # Use the latest 1 repetitive responses
            if len(text_of_recent_responses) >= 1:
                break

            if response.text in text_of_all_responses:
                text_of_recent_responses.add(response.text)

            text_of_all_responses.append(response.text)

        # Return the query with no changes if there are no statements to exclude
        if not text_of_recent_responses:
            return super(RepetitiveResponseFilter, self).filter_selection(
                chatterbot,
                conversation_id
            )

        print('text_of_recent_responses =>', text_of_recent_responses)

        query = chatterbot.storage.base_query.statement_text_not_in(
            text_of_recent_responses
        )

        return query
