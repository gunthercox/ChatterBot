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

        self.nlp = spacy.load(model)

    def get_text_index_string(self, text):
        """
        Return a string of text containing part-of-speech, lemma pairs.
        """
        bigram_pairs = []

        if len(text) <= 2:
            text_without_punctuation = text.translate(self.punctuation_table)
            if len(text_without_punctuation) >= 1:
                text = text_without_punctuation

        document = self.nlp(text)

        if len(text) <= 2:
            bigram_pairs = [
                token.lemma_.lower() for token in document
            ]
        else:
            tokens = [
                token for token in document if token.is_alpha and not token.is_stop
            ]

            if len(tokens) < 2:
                tokens = [
                    token for token in document if token.is_alpha
                ]

            for index in range(1, len(tokens)):
                bigram_pairs.append('{}:{}'.format(
                    tokens[index - 1].pos_,
                    tokens[index].lemma_.lower()
                ))

        if not bigram_pairs:
            bigram_pairs = [
                token.lemma_.lower() for token in document
            ]

        return ' '.join(bigram_pairs)
