import warnings
from .best_match import BestMatch


class SentimentAdapter(BestMatch):
    """
    This adapter selects a response with the closest
    matching sentiment value to the input statement.
    """

    def __init__(self, **kwargs):
        super(SentimentAdapter, self).__init__(**kwargs)
        from chatterbot.comparisons import sentiment_comparison

        self.compare_statements = kwargs.get(
            'statement_comparison_function',
            sentiment_comparison
        )

        warnings.warn(
            'The SentimentAdapter is deprecated. ' +
            'Use "chatterbot.logic.BestMatch" response_selection_method="chatterbot.comparisons.sentiment_comparison" instead.',
            DeprecationWarning
        )
