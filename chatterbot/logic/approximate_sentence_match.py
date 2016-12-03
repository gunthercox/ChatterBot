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
            'Use "chatterbot.logic.BestMatch" response_selection_method="chatterbot.conversation.comparisons.jaccard_similarity" instead.',
            DeprecationWarning
        )
