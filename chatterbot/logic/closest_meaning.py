import warnings
from .best_match import BestMatch


class ClosestMeaningAdapter(BestMatch):
    """
    This adapter selects a response by comparing the tokenized form of the
    input statement's text, with the tokenized form of possible matching
    statements. For each possible match, the sum of the Cartesian product of
    the path similarity of each statement is compared. This process simulates
    an evaluation of the closeness of synonyms. The known statement with the
    greatest path similarity is then returned.
    """

    def __init__(self, **kwargs):
        super(ClosestMeaningAdapter, self).__init__(**kwargs)
        from chatterbot.comparisons import synset_distance

        self.compare_statements = kwargs.get(
            'statement_comparison_function',
            synset_distance
        )

        warnings.warn(
            'The ClosestMeaningAdapter is deprecated. ' +
            'Use "chatterbot.logic.BestMatch" with response_selection_method="chatterbot.comparisons.synset_distance" instead.',
            DeprecationWarning
        )
