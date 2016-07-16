from chatterbot.filters import Filter


class LanguageFilter(Filter):
    """
    A filter that excludes swear words and explicit
    language from the selection of possible responses
    that a chat bot can respond with.
    """

    def filter_selection(self, statements):
        # TODO

        return statements
