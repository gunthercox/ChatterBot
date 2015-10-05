from .logic import LogicAdapter
from fuzzywuzzy import process


class ClosestMatchAdapter(LogicAdapter):

    def get(self, text, list_of_statements, current_conversation=None):
        """
        Takes a statement string and a list of statement strings.
        Returns the closest matching statement from the list.
        """

        # If the list is empty, return the statement
        if not list_of_statements:
            return text

        # Check if an exact match exists
        if text in list_of_statements:
            return text

        # Get the closest matching statement from the database
        return process.extract(text, list_of_statements, limit=1)[0][0]

