class KnownResponseMixin(object):

    def get_statements_with_known_responses(self):
        """
        Filter out all statements that are not in response to another statement.
        A statement must exist which lists the closest matching statement in the
        in_response_to field. Otherwise, the logic adapter may find a closest
        matching statement that does not have a known response.
        """
        if (not self.context) or (not self.context.storage):
            return []

        all_statements = self.context.storage.filter()

        responses = set()
        to_remove = list()
        for statement in all_statements:
            for response in statement.in_response_to:
                responses.add(response.text)
        for statement in all_statements:
            if statement.text not in responses:
                to_remove.append(statement)

        for statement in to_remove:
            all_statements.remove(statement)

        return all_statements


class ResponseSelectionMixin(object):

    def process(self, input_statement):

        # Select the closest match to the input statement
        closest_match = self.get(input_statement)

        # Save any updates made to the statement by the logic adapter
        self.context.storage.update(closest_match)

        # Get all statements that are in response to the closest match
        response_list = self.context.storage.filter(
            in_response_to__contains=closest_match.text
        )

        if response_list:
            if self.tie_breaking_method == "first_response":
                response = self.get_first_response(response_list)
            elif self.tie_breaking_method == "most_frequent_response":
                response = self.get_most_frequent_response(closest_match, response_list)
            else:
                response = self.get_random_response(response_list)
        else:
            response = self.storage.get_random()

        return response

    def get_most_frequent_response(self, input_statement, response_list):
        """
        Returns the statement with the greatest number of occurrences.
        """

        # Initialize the matching responce to the first response.
        # This will be returned in the case that no match can be found.
        matching_response = response_list[0]
        occurrence_count = 0

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

