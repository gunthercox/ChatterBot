from chatterbot.filters import Filter


class RepetitiveResponseFilter(Filter):
    """
    A filter that eliminates possibly repetitive
    responses to prevent a chat bot from repeating
    statements that it has recently said.
    """

    def filter_selection(self, statements):
        # TODO

        return statements
