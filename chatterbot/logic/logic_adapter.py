from __future__ import unicode_literals
from chatterbot.adapters import Adapter
from chatterbot.utils import import_module


class LogicAdapter(Adapter):
    """
    This is an abstract class that represents the interface
    that all logic adapters should implement.

    :param statement_comparison_function: The dot-notated import path to a statement comparison function.
                                          Defaults to ``levenshtein_distance``.

    :param response_selection_method: The a response selection method.
                                      Defaults to ``get_first_response``.
    """

    def __init__(self, **kwargs):
        super(LogicAdapter, self).__init__(**kwargs)
        from chatterbot.comparisons import levenshtein_distance
        from chatterbot.response_selection import get_first_response

        # Import string module parameters
        if 'statement_comparison_function' in kwargs:
            import_path = kwargs.get('statement_comparison_function')
            if isinstance(import_path, str):
                kwargs['statement_comparison_function'] = import_module(import_path)

        if 'response_selection_method' in kwargs:
            import_path = kwargs.get('response_selection_method')
            if isinstance(import_path, str):
                kwargs['response_selection_method'] = import_module(import_path)

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

    def get_initialization_functions(self):
        """
        Return a dictionary of functions to be run once when the chat bot is instantiated.
        """
        return self.compare_statements.get_initialization_functions()

    def initialize(self):
        for function in self.get_initialization_functions().values():
            function()

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

        :rtype: Statement
        """
        raise self.AdapterMethodNotImplementedError()

    @property
    def class_name(self):
        """
        Return the name of the current logic adapter class.
        This is typically used for logging and debugging.
        """
        return str(self.__class__.__name__)

    class EmptyDatasetException(Exception):

        def __init__(self, value='An empty set was received when at least one statement was expected.'):
            self.value = value

        def __str__(self):
            return repr(self.value)
