from .logic_adapter import LogicAdapter
from .mixins import TieBreaking


class BaseMatchAdapter(TieBreaking, LogicAdapter):
    """
    This is a parent class used by the ClosestMatch and
    ClosestMeaning adapters.
    """

    def __init__(self, **kwargs):
        super(BaseMatchAdapter, self).__init__(**kwargs)

        self.tie_breaking_method = kwargs.get(
            "tie_breaking_method",
            "first_response"
        )

    @property
    def has_storage_context(self):
        """
        Return true if the adapter has access to the storage adapter context.
        """
        return self.context and self.context.storage

    def get_available_statements(self, statement_list=None):
        from chatterbot.conversation.utils import get_response_statements

        if statement_list:
            statement_list = get_response_statements(statement_list)

        # Check if the list is empty
        if not statement_list and self.has_storage_context:
            all_statements = self.context.storage.filter()
            statement_list = get_response_statements(all_statements)

        return statement_list

    def get(self, input_statement, statement_list=None):
        """
        This method should be overridden with one to select a match
        based on the input statement.
        """
        raise self.AdapterMethodNotImplementedError()

    def can_process(self, statement):
        """
        Override the can_process method to check if the
        storage context is available and there is at least
        one statement in the database.
        """
        return self.has_storage_context and self.context.storage.count()

    def process(self, input_statement):

        # Select the closest match to the input statement
        confidence, closest_match = self.get(input_statement)

        # Save any updates made to the statement by the logic adapter
        self.context.storage.update(closest_match)

        # Get all statements that are in response to the closest match
        response_list = self.context.storage.filter(
            in_response_to__contains=closest_match.text
        )

        if response_list:
            response = self.break_tie(response_list, self.tie_breaking_method)
        else:
            response = self.context.storage.get_random()

        return confidence, response
