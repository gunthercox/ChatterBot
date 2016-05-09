from chatterbot.adapters.input import InputAdapter
from chatterbot.conversation import Statement
import sys

PY3 = sys.version_info[0] == 3

JSON = 'json'
TEXT = 'text'
OBJECT = 'object'
VALID_FORMATS = (JSON, TEXT, OBJECT, )


class VariableInputTypeAdapter(InputAdapter):

    def __init__(self, **kwargs):
        super(VariableInputTypeAdapter, self).__init__(**kwargs)

    def detect_type(self, statement):

        if PY3:
            string_types = str
        else:
            string_types = basestring

        if isinstance(statement, Statement):
            return OBJECT
        if isinstance(statement, string_types):
            return TEXT
        if isinstance(statement, dict):
            return JSON

        input_type = type(statement)

        raise self.UnrecognizedInputFormatException(
            'The type {} is not recognized as a valid input type.'.format(
                input_type
            )
        )

    def process_input(self, statement):
        input_type = self.detect_type(statement)

        # Return the statement object without modification
        if input_type == OBJECT:
            return statement

        # Convert the input string into a statement object
        if input_type == TEXT:
            return Statement(statement)

        # Convert input dictionary into a statement object
        if input_type == JSON:
            input_json = dict(statement)
            text = input_json["text"]
            del(input_json["text"])

            return Statement(text, **input_json)

    class UnrecognizedInputFormatException(Exception):
        def __init__(self, message='The input format was not recognized.'):
            super(
                VariableInputTypeAdapter.UnrecognizedInputFormatException,
                self
            ).__init__(message)

        def __str__(self):
            return self.message
