from .base_match import BaseMatchAdapter


class ApproximateSentenceMatchAdapter(BaseMatchAdapter):

    def __init__(self, **kwargs):
        super(ApproximateSentenceMatchAdapter, self).__init__(**kwargs)
        from chatterbot.conversation.comparisons import jaccard_similarity

        self.compare_statements = kwargs.get(
            'statement_comparison_function',
            jaccard_similarity
        )
