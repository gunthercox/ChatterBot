from __future__ import unicode_literals
from .logic_adapter import LogicAdapter


class SpecificResponseAdapter(LogicAdapter):
    """
    Return a specific response to a specific input.
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
        confidence = 0

        if statement == self.input_text:
            confidence = 1

        return confidence, self.response_statement
