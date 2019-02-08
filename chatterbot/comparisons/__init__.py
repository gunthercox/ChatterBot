
"""
This module contains various text-comparison algorithms
designed to compare one statement to another.
"""

from .levenshtein_distance import LevenshteinDistance
from .synset_distance import SynsetDistance
from .sentiment_comparison import SentimentComparison
from .jaccard_similarity import JaccardSimilarity
from .embedded_wordvector import EmbeddedWordVector

levenshtein_distance = LevenshteinDistance()
synset_distance = SynsetDistance()
sentiment_comparison = SentimentComparison()
jaccard_similarity = JaccardSimilarity()
embedded_wordvector = EmbeddedWordVector()


__all__ = (
    'levenshtein_distance',
    'synset_distance',
    'sentiment_comparison',
    'jaccard_similarity',
    'embedded_wordvector'
)
