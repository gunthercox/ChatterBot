from .logic import LogicAdapter
from fuzzywuzzy import process


class ClosestMatchAdapter(LogicAdapter):

    def get(self, text, statement_list, current_conversation=None):
        """
        Takes a statement string and a list of statement strings.
        Returns the closest matching statement from the list.
        """

        # Get the text of each statement
        text_of_all_statements = []
        for statement in statement_list:
            text_of_all_statements.append(statement.text)

        # If the list is empty, return the statement
        if not text_of_all_statements:
            return text

        # Check if an exact match exists
        if text in text_of_all_statements:
            return text

        # Get the closest matching statement from the database
        return process.extract(text, text_of_all_statements, limit=1)[0][0]

