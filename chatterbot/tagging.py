from typing import List, Union, Tuple
from chatterbot import languages
from chatterbot.utils import get_model_for_language
import spacy


class NoOpTagger(object):
    """
    A no-operation tagger that returns text unchanged.
    Used by storage adapters that don't rely on indexed search_text fields.
    """

    def __init__(self, language=None):
        self.language = language or languages.ENG

    def get_text_index_string(self, text: Union[str, List[str]]):
        """
        Return the text unchanged (no indexing applied).
        """
        return text

    def as_nlp_pipeline(
        self,
        texts: Union[List[str], Tuple[str, dict]],
        batch_size: int = 1000,
        n_process: int = 1
    ):
        """
        Returns texts unchanged without NLP processing.
        Maintains API compatibility with other taggers.

        :param texts: Text strings or tuples of (text, context_dict)
        :param batch_size: Ignored (for API compatibility)
        :param n_process: Ignored (for API compatibility)
        """
        process_as_tuples = texts and isinstance(texts[0], tuple)

        if process_as_tuples:
            # Return generator of (text, context) tuples
            for text, context in texts:
                yield (text, context)
        else:
            # Return generator of text strings
            for text in texts:
                yield text


class LowercaseTagger(object):
    """
    Returns the text in lowercase.
    """

    def __init__(self, language=None):
        from chatterbot.components import chatterbot_lowercase_indexer  # noqa

        self.language = language or languages.ENG

        # Create a new empty spacy nlp object
        self.nlp = spacy.blank(self.language.ISO_639_1)

        self.nlp.add_pipe(
            'chatterbot_lowercase_indexer', name='chatterbot_lowercase_indexer', last=True
        )

    def get_text_index_string(self, text: Union[str, List[str]]):
        if isinstance(text, list):
            documents = self.nlp.pipe(text, batch_size=1000, n_process=1)
            return [document._.search_index for document in documents]
        else:
            document = self.nlp(text)
            return document._.search_index

    def as_nlp_pipeline(
        self,
        texts: Union[List[str], Tuple[str, dict]],
        batch_size: int = 1000,
        n_process: int = 1
    ):
        """
        Process texts through the spaCy NLP pipeline with optimized batching.

        :param texts: Text strings or tuples of (text, context_dict)
        :param batch_size: Number of texts per batch (default 1000)
        :param n_process: Number of worker processes for spaCy's pipe (set >1 to use multiprocessing)

        Usage:
            documents = tagger.as_nlp_pipeline(texts)
            documents = tagger.as_nlp_pipeline(texts, batch_size=2000, n_process=4)
        """
        process_as_tuples = texts and isinstance(texts[0], tuple)

        documents = self.nlp.pipe(
            texts,
            as_tuples=process_as_tuples,
            batch_size=batch_size,
            n_process=n_process
        )
        return documents


class PosLemmaTagger(object):

    def __init__(self, language=None):
        from chatterbot.components import chatterbot_bigram_indexer  # noqa

        self.language = language or languages.ENG

        model = get_model_for_language(self.language)

        # Disable the Named Entity Recognition (NER) component because it is not necessary
        self.nlp = spacy.load(model, exclude=['ner'])

        self.nlp.add_pipe(
            'chatterbot_bigram_indexer', name='chatterbot_bigram_indexer', last=True
        )

    def get_text_index_string(self, text: Union[str, List[str]]) -> str:
        """
        Return a string of text containing part-of-speech, lemma pairs.
        """
        if isinstance(text, list):
            documents = self.nlp.pipe(text, batch_size=1000, n_process=1)
            return [document._.search_index for document in documents]
        else:
            document = self.nlp(text)
            return document._.search_index

    def as_nlp_pipeline(
        self,
        texts: Union[List[str], Tuple[str, dict]],
        batch_size: int = 1000,
        n_process: int = 1
    ) -> spacy.tokens.Doc:
        """
        Accepts a single string or a list of strings, or a list of tuples
        where the first element is the text and the second element is a
        dictionary of context to return alongside the generated document.

        :param texts: Text strings or tuples of (text, context_dict)
        :param batch_size: Number of texts per batch (default 1000)
        :param n_process: Number of worker processes for spaCy's pipe (set >1 to use multiprocessing)

        Usage:
            documents = tagger.as_nlp_pipeline(texts)
            documents = tagger.as_nlp_pipeline(texts, batch_size=2000, n_process=4)
        """
        process_as_tuples = texts and isinstance(texts[0], tuple)

        documents = self.nlp.pipe(
            texts,
            as_tuples=process_as_tuples,
            batch_size=batch_size,
            n_process=n_process
        )
        return documents
