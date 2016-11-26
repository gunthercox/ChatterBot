from __future__ import unicode_literals
from .logic_adapter import LogicAdapter


class BaseMatchAdapter(LogicAdapter):
    """
    This is a parent class used by the ClosestMatch and
    ClosestMeaning adapters.
    """

    @property
    def has_storage(self):
        """
        Return true if the adapter has access to the chatbot's storage adapter.
        """
        return self.chatbot and self.chatbot.storage

    def get(self, input_statement):
        """
        Takes a statement string and a list of statement strings.
        Returns the closest matching statement from the list.
        """
        statement_list = self.chatbot.storage.get_response_statements()

        if not statement_list:
            if self.has_storage:
                # Use a randomly picked statement
                self.logger.info(
                    'No statements have known responses. ' +
                    'Choosing a random response to return.'
                )
                return 0, self.chatbot.storage.get_random()
            else:
                raise self.EmptyDatasetException()

        closest_match = input_statement
        max_confidence = 0

        # Find the closest matching known statement
        for statement in statement_list:
            confidence = self.compare_statements(input_statement, statement)

            if confidence > max_confidence:
                max_confidence = confidence
                closest_match = statement

        return max_confidence, closest_match

    def can_process(self, statement):
        """
        Check that the chatbot's storage adapter is available to the logic adapter
        and there is at least one statement in the database.
        """
        return self.has_storage and self.chatbot.storage.count()

    def process(self, input_statement):

        # Select the closest match to the input statement
        confidence, closest_match = self.get(input_statement)
        self.logger.info('Using "{}" as a close match to "{}"'.format(
            input_statement.text, closest_match.text
        ))

        # Save any updates made to the statement by the logic adapter
        self.chatbot.storage.update(closest_match)

        # Get all statements that are in response to the closest match
        response_list = self.chatbot.storage.filter(
            in_response_to__contains=closest_match.text
        )

        if response_list:
            self.logger.info(
                'Selecting response from {} optimal responses.'.format(
                    len(response_list)
                )
            )
            response = self.select_response(input_statement, response_list)
            self.logger.info('Response selected. Using "{}"'.format(response.text))
        else:
            response = self.chatbot.storage.get_random()
            self.logger.info(
                'No response to "{}" found. Selecting a random response.'.format(
                    closest_match.text
                )
            )

            # Set confidence to zero because a random response is selected
            confidence = 0

        return confidence, response
