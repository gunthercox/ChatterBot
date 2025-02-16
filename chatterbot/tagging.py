import string
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

        self.language = language or languages.ENG

        self.punctuation_table = str.maketrans(dict.fromkeys(string.punctuation))

        try:
            model = constants.DEFAULT_LANGUAGE_TO_SPACY_MODEL_MAP[self.language]
        except KeyError as e:
            raise KeyError(
                f'Spacy model is not available for language {self.language}'
            ) from e

        # Disable the Named Entity Recognition (NER) component because it is not necessary
        self.nlp = spacy.load(model, exclude=['ner'])

    def _get_bigram_pairs(self, document):
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
                self.punctuation_table
            )
            if len(text_without_punctuation) >= 1:
                text = text_without_punctuation.lower()
            else:
                text = document.text.lower()

            bigram_pairs = [text]

        return bigram_pairs

    def get_text_index_string(self, text):
        """
        Return a string of text containing part-of-speech, lemma pairs.
        """
        if isinstance(text, list):
            documents = self.nlp.pipe(text)
            return [' '.join(self._get_bigram_pairs(document)) for document in documents]
        else:
            document = self.nlp(text)
            bigram_pairs = self._get_bigram_pairs(document)
            return ' '.join(bigram_pairs)
