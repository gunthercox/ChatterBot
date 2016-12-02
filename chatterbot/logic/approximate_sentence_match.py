import warnings
from .best_match import BestMatch


class ApproximateSentenceMatchAdapter(BestMatch):

    def __init__(self, **kwargs):
        super(ApproximateSentenceMatchAdapter, self).__init__(**kwargs)
        from chatterbot.conversation.comparisons import jaccard_similarity

        self.compare_statements = kwargs.get(
            'statement_comparison_function',
            jaccard_similarity
        )

        warnings.warn(
            'The ApproximateSentenceMatchAdapter is deprecated. ' +
            'See http://chatterbot.readthedocs.io/en/latest/logic/index.html#best-match-adapter ' +
            'for details on how to update your code.',
            DeprecationWarning
        )
