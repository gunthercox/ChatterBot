class TieBreaking(object):
    """
    TieBreaking determines which response should be used in the event
    that multiple responses are generated within a logic adapter.
    """

    def break_tie(self, statement_list, method):

        METHODS = {
            "first_response": self.get_first_response,
            "random_response": self.get_random_response,
            "most_frequent_response": self.get_most_frequent_response
        }

        if method in METHODS:
            return METHODS[method](statement_list)

        # Default to the first method if an invalid method is passed in
        return METHODS["first_response"](statement_list)

    def get_most_frequent_response(self, input_statement, response_list):
        """
        Returns the statement with the greatest number of occurrences.
        """
        matching_response = None
        occurrence_count = -1

        for statement in response_list:
            count = statement.get_response_count(input_statement)

            # Keep the more common statement
            if count >= occurrence_count:
                matching_response = statement
                occurrence_count = count

        # Choose the most commonly occuring matching response
        return matching_response

    def get_first_response(self, response_list):
        """
        Return the first statement in the response list.
        """
        return response_list[0]

    def get_random_response(self, response_list):
        """
        Choose a random response from the selection.
        """
        from random import choice
        return choice(response_list)
