"""
Custom components for Spacy processing pipelines.
https://spacy.io/usage/processing-pipelines#custom-components
"""
import string
from spacy.language import Language
from spacy.tokens import Doc


punctuation_table = str.maketrans(dict.fromkeys(string.punctuation))


@Language.component('chatterbot_bigram_indexer')
def chatterbot_bigram_indexer(document):
    """
    Generate the text string for a bigram-based search index.
    """

    if not Doc.has_extension('search_index'):
        Doc.set_extension('search_index', default='')

    tokens = [
        token for token in document if not (token.is_punct or token.is_stop)
    ]

    # Fall back to including stop words if needed
    if not tokens or len(tokens) == 1:
        tokens = [
            token for token in document if not (token.is_punct)
        ]

    bigram_pairs = [
        f"{tokens[i - 1].pos_}:{tokens[i].lemma_.lower()}"
        for i in range(1, len(tokens))
    ]

    if not bigram_pairs:

        text_without_punctuation = document.text.translate(
            punctuation_table
        )
        if len(text_without_punctuation) >= 1:
            text = text_without_punctuation.lower()
        else:
            text = document.text.lower()

        bigram_pairs = [text]

    # Assign a custom attribute at the Doc level
    document._.search_index = ' '.join(bigram_pairs)

    return document


@Language.component('chatterbot_lowercase_indexer')
def chatterbot_lowercase_indexer(document):
    """
    Generate the a lowercase text string for search index.
    """

    if not Doc.has_extension('search_index'):
        Doc.set_extension('search_index', default='')

    # Assign a custom attribute at the Doc level
    document._.search_index = document.text.lower()

    return document
