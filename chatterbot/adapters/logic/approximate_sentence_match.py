# -*- coding: utf-8 -*-
from .base_match import BaseMatchAdapter


class ApproximateSentenceMatchAdapter(BaseMatchAdapter):

    def __init__(self, **kwargs):
        super(ClosestMatchAdapter, self).__init__(**kwargs)
        from chatterbot.conversation.comparisons import jaccard_similarity

        self.compare_statements = kwargs.get(
            'statement_comparison_function',
            jaccard_similarity
        )

    def get(self, input_statement):
        """
        Takes a statement string and a list of statement strings.
        Returns the closest matching statement from the list.
        """
        statement_list = self.context.storage.get_response_statements()

        if not statement_list:
            if self.has_storage_context:
                # Use a randomly picked statement
                return 0, self.context.storage.get_random()
            else:
                raise self.EmptyDatasetException()

        confidence = -1
        sentence_match = input_statement
        # Find the matching known statement
        for statement in statement_list:
            ratio = self.compare_statements(input_statement, statement)
            if ratio:
                closest_match = statement
            else:
                closest_match = statement
        return 0.5, closest_match
