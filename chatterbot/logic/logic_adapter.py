from chatterbot.adapters import Adapter
from chatterbot.storage import StorageAdapter
from chatterbot.search import IndexedTextSearch
from chatterbot.conversation import Statement


class LogicAdapter(Adapter):
    """
    This is an abstract class that represents the interface
    that all logic adapters should implement.

    :param search_algorithm_name: The name of the search algorithm that should
        be used to search for close matches to the provided input.
        Defaults to the value of ``Search.name``.

    :param maximum_similarity_threshold:
        The maximum amount of similarity between two statement that is required
        before the search process is halted. The search for a matching statement
        will continue until a statement with a greater than or equal similarity
        is found or the search set is exhausted.
        Defaults to 0.95

    :param response_selection_method:
          The a response selection method.
          Defaults to ``get_first_response``
    :type response_selection_method: collections.abc.Callable

    :param default_response:
          The default response returned by this logic adaper
          if there is no other possible response to return.
    :type default_response: str or list or tuple
    """

    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)
        from chatterbot.response_selection import get_first_response

        self.search_algorithm_name = kwargs.get(
            'search_algorithm_name',
            IndexedTextSearch.name
        )

        self.search_algorithm = self.chatbot.search_algorithms[
            self.search_algorithm_name
        ]

        self.maximum_similarity_threshold = kwargs.get(
            'maximum_similarity_threshold', 0.95
        )

        # By default, select the first available response
        self.select_response = kwargs.get(
            'response_selection_method',
            get_first_response
        )

        default_responses = kwargs.get('default_response', [])

        # Convert a single string into a list
        if isinstance(default_responses, str):
            default_responses = [
                default_responses
            ]

        self.default_responses = [
            Statement(text=default) for default in default_responses
        ]

    def can_process(self, statement):
        """
        A preliminary check that is called to determine if a
        logic adapter can process a given statement. By default,
        this method returns true but it can be overridden in
        child classes as needed.

        :rtype: bool
        """
        return True

    def process(self, statement, additional_response_selection_parameters=None):
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

        :param additional_response_selection_parameters: Parameters to be used when
            filtering results to choose a response from.
        :type additional_response_selection_parameters: dict

        :rtype: Statement
        """
        raise self.AdapterMethodNotImplementedError()

    def get_default_response(self, input_statement):
        """
        This method is called when a logic adapter is unable to generate any
        other meaningful response.
        """
        from random import choice

        if self.default_responses:
            response = choice(self.default_responses)
        else:
            try:
                response = self.chatbot.storage.get_random()
            except StorageAdapter.EmptyDatabaseException:
                response = input_statement

        self.chatbot.logger.info(
            'No known response to the input was found. Selecting a random response.'
        )

        # Set confidence to zero because a random response is selected
        response.confidence = 0

        return response

    @property
    def class_name(self):
        """
        Return the name of the current logic adapter class.
        This is typically used for logging and debugging.
        """
        return str(self.__class__.__name__)
