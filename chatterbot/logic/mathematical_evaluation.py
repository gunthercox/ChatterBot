from chatterbot.logic import LogicAdapter
from chatterbot.conversation import Statement
from chatterbot import languages


class MathematicalEvaluation(LogicAdapter):
    """
    The MathematicalEvaluation logic adapter parses input to determine
    whether the user is asking a question that requires math to be done.
    If so, the equation is extracted from the input and returned with
    the evaluated result.

    For example:
        User: 'What is three plus five?'
        Bot: 'Three plus five equals eight'

    :kwargs:
        * *language* (``object``) --
          The language is set to ``chatterbot.languages.ENG`` for English by default.
    """

    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)

        self.language = kwargs.get('language', languages.ENG)
        self.cache = {}

    def can_process(self, statement) -> bool:
        """
        Determines whether it is appropriate for this
        adapter to respond to the user input.
        """
        response = self.process(statement)
        self.cache[statement.text] = response
        return response.confidence == 1

    def process(self, statement: Statement, additional_response_selection_parameters: dict = None) -> Statement:
        """
        Takes a statement string.
        Returns the equation from the statement with the mathematical terms solved.
        """
        from mathparse import mathparse

        input_text = statement.text

        # Use the result cached by the process method if it exists
        if input_text in self.cache:
            cached_result = self.cache[input_text]
            self.cache = {}
            return cached_result

        # Getting the mathematical terms within the input statement
        expression = mathparse.extract_expression(input_text, language=self.language.ISO_639.upper())

        response = Statement(text=expression)

        try:
            response.text = '{} = {}'.format(
                response.text,
                mathparse.parse(expression, language=self.language.ISO_639.upper())
            )

            # The confidence is 1 if the expression could be evaluated
            response.confidence = 1
        except mathparse.PostfixTokenEvaluationException:
            response.confidence = 0

        return response
