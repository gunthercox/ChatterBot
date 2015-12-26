from chatterbot.adapters.exceptions import EmptyDatasetException
from chatterbot.adapters.logic.mixins import KnownResponseMixin, ResponseSelectionMixin
from .logic import LogicAdapter
from fuzzywuzzy import process


class ClosestMatchAdapter(ResponseSelectionMixin, KnownResponseMixin, LogicAdapter):

    def get(self, input_statement, statement_list=None):
        """
        Takes a statement string and a list of statement strings.
        Returns the closest matching statement from the list.
        """

        if not statement_list:
            statement_list = self.get_statements_with_known_responses()

        # Check if the list is empty
        if not statement_list:
            if self.context and self.context.storage:
                # Use a randomly picked statement
                return self.context.storage.get_random()
            else:
                raise EmptyDatasetException

        # Get the text of each statement
        text_of_all_statements = []
        for statement in statement_list:
            text_of_all_statements.append(statement.text)

        # Check if an exact match exists
        if input_statement.text in text_of_all_statements:
            return input_statement

        # Get the closest matching statement from the database
        closest_match = process.extract(
            input_statement.text,
            text_of_all_statements,
            limit=1
        )[0][0]

        return next((s for s in statement_list if s.text == closest_match), None)

