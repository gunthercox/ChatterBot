# -*- coding: utf-8 -*-
from .base_match import BaseMatchAdapter


class ClosestMatchAdapter(BaseMatchAdapter):
    """
    The ClosestMatchAdapter logic adapter selects a known response
    to an input by searching for a known statement that most closely
    matches the input based on the Levenshtein Distance between the text
    of each statement.
    """

    def __init__(self, **kwargs):
        super(ClosestMatchAdapter, self).__init__(**kwargs)
        from chatterbot.conversation.comparisons import levenshtein_distance

        self.compare_statements = kwargs.get(
            'statement_comparison_function',
            levenshtein_distance
        )