from chatterbot.adapters.input import InputAdapter
from chatterbot.utils.read_input import input_function
from chatterbot.conversation import Statement


JSON = 'json'
TEXT = 'text'
OBJECT = 'object'
VALID_FORMATS = (JSON, TEXT, OBJECT, )


class VariableInputTypeAdapter(InputAdapter):

    def __init__(self, **kwargs):
        super(VariableInputTypeAdapter, self).__init__(**kwargs)

    def detect_type(self, statement):
        input_type = type(statement)

        if input_type is Statement:
            return OBJECT
        if input_type is str:
            return TEXT
        if input_type is dict:
            return JSON

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
