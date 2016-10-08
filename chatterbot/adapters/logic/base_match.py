# -*- coding: utf-8 -*-
from .logic_adapter import LogicAdapter
from .mixins import TieBreaking


class BaseMatchAdapter(TieBreaking, LogicAdapter):
    """
    This is a parent class used by the ClosestMatch and
    ClosestMeaning adapters.
    """

    def __init__(self, **kwargs):
        super(BaseMatchAdapter, self).__init__(**kwargs)
        from chatterbot.conversation.comparisons import levenshtein_distance

        self.tie_breaking_method = kwargs.get(
            "tie_breaking_method",
            "first_response"
        )

        self.compare_statements = kwargs.get(
            'statement_comparison_function',
            levenshtein_distance
        )

    @property
    def has_storage_context(self):
        """
        Return true if the adapter has access to the storage adapter context.
        """
        return self.context and self.context.storage

    def get(self, input_statement):
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
        self.logger.info(u'Using "{}" as a close match to "{}"'.format(
            input_statement.text, closest_match.text
        ))

        # Save any updates made to the statement by the logic adapter
        self.context.storage.update(closest_match)

        # Get all statements that are in response to the closest match
        response_list = self.context.storage.filter(
            in_response_to__contains=closest_match.text
        )

        if response_list:
            self.logger.info(
                u'Breaking tie between {} optimal responses.'.format(
                    len(response_list)
                )
            )
            response = self.break_tie(input_statement, response_list, self.tie_breaking_method)
            self.logger.info(u'Tie broken. Using "{}"'.format(response.text))
        else:
            response = self.context.storage.get_random()
            self.logger.info(
                u'No response to "{}" found. Using a random response.'.format(
                    closest_match.text
                )
            )

            # Set confidence to zero if a random response is selected
            confidence = 0

        return confidence, response
