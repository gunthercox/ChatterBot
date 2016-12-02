import warnings
from .best_match import BestMatch


class SentimentAdapter(BestMatch):
    """
    This adapter selects a response with the closest
    matching sentiment value to the input statement.
    """

    def __init__(self, **kwargs):
        super(SentimentAdapter, self).__init__(**kwargs)
        from chatterbot.conversation.comparisons import sentiment_comparison

        self.compare_statements = kwargs.get(
            'statement_comparison_function',
            sentiment_comparison
        )

        warnings.warn(
            'The SentimentAdapter is deprecated. ' +
            'See http://chatterbot.readthedocs.io/en/latest/logic/index.html#best-match-adapter ' +
            'for details on how to update your code.',
            DeprecationWarning
        )
