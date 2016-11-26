from .base_match import BaseMatchAdapter


class SentimentAdapter(BaseMatchAdapter):
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
