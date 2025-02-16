from chatterbot import languages, constants


class LowercaseTagger(object):
    """
    Returns the text in lowercase.
    """

    def __init__(self, language=None):
        self.language = language or languages.ENG

    def get_text_index_string(self, text):
        return text.lower()


class PosLemmaTagger(object):

    def __init__(self, language=None):
        import spacy
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
            return [document._.bigram_index for document in documents]
        else:
            document = self.nlp(text)
            return document._.bigram_index
