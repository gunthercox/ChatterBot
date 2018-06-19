from .logic_adapter import LogicAdapter


class SpecificResponseAdapter(LogicAdapter):
    """
    Return a specific response to a specific input.

    :kwargs:
        * *input_text* (``str``) --
          The input text that triggers this logic adapter.
        * *output_text* (``str``) --
          The output text returned by this logic adapter.
    """

    def __init__(self, **kwargs):
        super(SpecificResponseAdapter, self).__init__(**kwargs)
        from chatterbot.conversation import Statement

        self.input_text = kwargs.get('input_text')

        output_text = kwargs.get('output_text')
        self.response_statement = Statement(output_text)

    def can_process(self, statement):
        if statement == self.input_text:
            return True

        return False

    def process(self, statement):

        if statement == self.input_text:
            self.response_statement.confidence = 1
        else:
            self.response_statement.confidence = 0

        return self.response_statement
