# -*- coding: utf-8 -*-
from fuzzywuzzy import fuzz
from .base_match import BaseMatchAdapter


class ClosestMatchAdapter(BaseMatchAdapter):
    """
    The ClosestMatchAdapter logic adapter selects a known response
    to an input by searching for a known statement that most closely
    matches the input based on the Levenshtein Distance between the text
    of each statement.
    """

    def get(self, input_statement):
        """
        Takes a statement string and a list of statement strings.
        Returns the closest matching statement from the list.
        """
        statement_list = self.context.storage.get_response_statements()

        if not statement_list:
            if self.has_storage_context:
                # Use a randomly picked statement
                self.logger.info(
                    u'No statements have known responses. ' +
                    u'Choosing a random response to return.'
                )
                return 0, self.context.storage.get_random()
            else:
                raise self.EmptyDatasetException()

        closest_match = input_statement
        closest_similarity = -1

        # Find the closest matching known statement
        for statement in statement_list:
            similarity = self.compare_statements(input_statement, statement)

            if similarity > closest_similarity:
                closest_similarity = similarity
                closest_match = statement

        # Convert the confidence integer to a percent
        confidence = closest_similarity / 100.0

        return confidence, closest_match
