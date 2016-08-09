# Filters set the base query that gets passed to the storage adapter


class Filter(object):
    """
    A base filter object from which all other
    filters should be subclassed.
    """

    def filter_selection(self, query, context):
        return query


class StatementsWithResponsesFilter(Filter):
    """
    
    """

    def filter_selection(self, query, context):
        # TODO

        return query

class RepetitiveResponseFilter(Filter):
    """
    A filter that eliminates possibly repetitive
    responses to prevent a chat bot from repeating
    statements that it has recently said.
    """

    def filter_selection(self, query, context):

        # TODO
        query = context.storage.query.not_in(
            query,
            self.recent_responses
        )

        return query


class LanguageFilter(Filter):
    """
    A filter that excludes swear words and explicit
    language from the selection of possible responses
    that a chat bot can respond with.
    """

    def __init__(self):
        self.words = (
            'dammit', 'retard', 'fuck', 'fucking',
        )
        # TODO: Load from data file
        # TODO: Unzip/decrypt? data file on first use?

    def filter_selection(self, query, context):
        return context.storage.query.not_in(
            self.words,
            query
        )
