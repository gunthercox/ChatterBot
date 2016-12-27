"""
This file provides proxy methods for backwards compatability.
"""
import warnings

from chatterbot.comparisons import levenshtein_distance
from chatterbot.comparisons import synset_distance
from chatterbot.comparisons import sentiment_comparison
from chatterbot.comparisons import jaccard_similarity

warnings.warn(
    'The module "chatterbot.conversation.comparisons has moved." ' +
    'Use "chatterbot.comparisons" instead.',
    DeprecationWarning
)
