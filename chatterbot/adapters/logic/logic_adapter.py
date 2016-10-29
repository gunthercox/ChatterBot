from chatterbot.adapters import Adapter


class LogicAdapter(Adapter):
    """
    This is an abstract class that represents the interface
    that all logic adapters should implement.
    """

    def __init__(self, **kwargs):
        super(LogicAdapter, self).__init__(**kwargs)
        from chatterbot.conversation.comparisons import levenshtein_distance
        from chatterbot.conversation.response_selection import get_first_response

        # By default, compare statements using Levenshtein distance
        self.compare_statements = kwargs.get(
            'statement_comparison_function',
            levenshtein_distance
        )

        # By default, select the first available response
        self.select_response = kwargs.get(
            'response_selection_method',
            get_first_response
        )

    def can_process(self, statement):
        """
        A preliminary check that is called to determine if a
        logic adapter can process a given statement. By default,
        this method returns true but it can be overridden in
        child classes as needed.
        """
        return True

    def process(self, statement):
        """
        Method that takes an input statement and returns
        a confidence value and a statement as output.
        """
        raise self.AdapterMethodNotImplementedError()

    class EmptyDatasetException(Exception):

        def __init__(self, value="An empty set was received when at least one statement was expected."):
            self.value = value

        def __str__(self):
            return repr(self.value)
