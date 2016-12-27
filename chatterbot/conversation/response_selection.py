"""
This file provides proxy methods for backwards compatability.
"""
import warnings

from chatterbot.response_selection import get_most_frequent_response
from chatterbot.response_selection import get_first_response
from chatterbot.response_selection import get_random_response

warnings.warn(
    'The module "chatterbot.conversation.response_selection has moved." ' +
    'Use "chatterbot.response_selection" instead.',
    DeprecationWarning
)
