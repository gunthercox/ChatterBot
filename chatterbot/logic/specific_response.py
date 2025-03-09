from chatterbot.logic import LogicAdapter
from chatterbot.conversation import Statement
from chatterbot import constants, languages
import spacy


class SpecificResponseAdapter(LogicAdapter):
    """
    Return a specific response to a specific input.

    :kwargs:
        * *input_text* (``str``) --
          The input text that triggers this logic adapter.
        * *output_text* (``str`` or ``function``) --
          The output text returned by this logic adapter.
          If a function is provided, it should return a string.
    """

    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)

        self.input_text = kwargs.get('input_text')

        self.matcher = None

        if MatcherClass := kwargs.get('matcher'):
            language = kwargs.get('language', languages.ENG)

            self.nlp = self._initialize_nlp(language)

            self.matcher = MatcherClass(self.nlp.vocab)

            self.matcher.add('SpecificResponse', [self.input_text])

        self._output_text = kwargs.get('output_text')

    def _initialize_nlp(self, language):
        try:
            model = constants.DEFAULT_LANGUAGE_TO_SPACY_MODEL_MAP[language]
        except KeyError as e:
            raise KeyError(
                f'Spacy model is not available for language {language}'
            ) from e

        return spacy.load(model)

    def can_process(self, statement):
        if self.matcher:
            doc = self.nlp(statement.text)
            matches = self.matcher(doc)

            if matches:
                return True
        elif statement.text == self.input_text:
            return True

        return False

    def process(self, statement, additional_response_selection_parameters=None):

        if callable(self._output_text):
            response_statement = Statement(text=self._output_text())
        else:
            response_statement = Statement(text=self._output_text)

        if self.matcher:
            doc = self.nlp(statement.text)
            matches = self.matcher(doc)

            if matches:
                response_statement.confidence = 1
            else:
                response_statement.confidence = 0

        elif statement.text == self.input_text:
            response_statement.confidence = 1
        else:
            response_statement.confidence = 0

        return response_statement
