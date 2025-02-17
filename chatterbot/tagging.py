from chatterbot import languages, constants
import spacy


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

    def get_text_index_string(self, text):
        if isinstance(text, list):
            documents = self.nlp.pipe(text)
            return [document._.search_index for document in documents]
        else:
            document = self.nlp(text)
            return document._.search_index

    def as_nlp_pipeline(self, texts):

        process_as_tuples = texts and isinstance(texts[0], tuple)

        documents = self.nlp.pipe(texts, as_tuples=process_as_tuples)
        return documents


class PosLemmaTagger(object):

    def __init__(self, language=None):
        from chatterbot.components import chatterbot_bigram_indexer  # noqa

        self.language = language or languages.ENG

        try:
            model = constants.DEFAULT_LANGUAGE_TO_SPACY_MODEL_MAP[self.language]
        except KeyError as e:
            raise KeyError(
                f'Spacy model is not available for language {self.language}'
            ) from e

        # Disable the Named Entity Recognition (NER) component because it is not necessary
        self.nlp = spacy.load(model, exclude=['ner'])

        self.nlp.add_pipe(
            'chatterbot_bigram_indexer', name='chatterbot_bigram_indexer', last=True
        )

    def get_text_index_string(self, text):
        """
        Return a string of text containing part-of-speech, lemma pairs.
        """
        if isinstance(text, list):
            documents = self.nlp.pipe(text)
            return [document._.search_index for document in documents]
        else:
            document = self.nlp(text)
            return document._.search_index

    def as_nlp_pipeline(self, texts):
        """
        Accepts a single string or a list of strings, or a list of tuples
        where the first element is the text and the second element is a
        dictionary of context to return alongside the generated document.
        """

        process_as_tuples = texts and isinstance(texts[0], tuple)

        documents = self.nlp.pipe(texts, as_tuples=process_as_tuples)
        return documents
