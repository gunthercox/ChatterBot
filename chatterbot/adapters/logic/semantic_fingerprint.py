from .logic import LogicAdapter


class SemanticFingerprintAdapter(LogicAdapter):

    def get(self, text, list_of_statements):
        """
        Takes a statement string and a list of statement strings.
        Returns the closest matching statement from the list.
        """

        # Get the closest matching statement
        closest_matching = text

        # Returning the closest matching statement
        return closest_matching
