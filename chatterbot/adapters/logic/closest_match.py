from chatterbot.adapters.exceptions import EmptyDatasetException
from .logic import LogicAdapter
from fuzzywuzzy import process


class ClosestMatchAdapter(LogicAdapter):

    def get(self, input_statement, statement_list):
        """
        Takes a statement string and a list of statement strings.
        Returns the closest matching statement from the list.
        """

        # Check if the list is empty
        if not statement_list:
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

