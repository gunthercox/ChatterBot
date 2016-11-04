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

        if 'tie_breaking_method' in kwargs:
            raise DeprecationWarning(
                'The parameter "tie_breaking_method" has been removed. ' +
                'Instead, pass a callable to "response_selection_method". ' +
                'See documentation for details: ' +
                'http://chatterbot.readthedocs.io/en/latest/adapters/response_selection.html#setting-the-response-selection-method'
            )

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

        :rtype: bool
        """
        return True

    def process(self, statement):
        """
        Override this method and implement your logic for selecting a response to an input statement.

        A confidence value and the selected response statement should be returned.
        The confidence value represents a rating of how accurate the logic adapter
        expects the selected response to be. Confidence scores are used to select
        the best response from multiple logic adapters.

        The confidence value should be a number between 0 and 1 where 0 is the
        lowest confidence level and 1 is the highest.

        :param statement: An input statement to be processed by the logic adapter.
        :type statement: Statement

        :rtype: float, Statement
        """
        raise self.AdapterMethodNotImplementedError()

    class EmptyDatasetException(Exception):

        def __init__(self, value="An empty set was received when at least one statement was expected."):
            self.value = value

        def __str__(self):
            return repr(self.value)
