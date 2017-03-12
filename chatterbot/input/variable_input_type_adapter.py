from __future__ import unicode_literals
from chatterbot.input import InputAdapter
from chatterbot.conversation import Statement


class VariableInputTypeAdapter(InputAdapter):

    JSON = 'json'
    TEXT = 'text'
    OBJECT = 'object'
    VALID_FORMATS = (JSON, TEXT, OBJECT, )

    def __init__(self, **kwargs):
        super(VariableInputTypeAdapter, self).__init__(**kwargs)

    def detect_type(self, statement):
        import sys

        if sys.version_info[0] == 3:
            string_types = str
        else:
            string_types = basestring

        if hasattr(statement, 'text'):
            return self.OBJECT
        if isinstance(statement, string_types):
            return self.TEXT
        if isinstance(statement, dict):
            return self.JSON

        input_type = type(statement)

        raise self.UnrecognizedInputFormatException(
            'The type {} is not recognized as a valid input type.'.format(
                input_type
            )
        )

    def process_input(self, statement):
        input_type = self.detect_type(statement)

        # Return the statement object without modification
        if input_type == self.OBJECT:
            return statement

        # Convert the input string into a statement object
        if input_type == self.TEXT:
            return Statement(statement)

        # Convert input dictionary into a statement object
        if input_type == self.JSON:
            input_json = dict(statement)
            text = input_json["text"]
            del(input_json["text"])

            return Statement(text, **input_json)

    class UnrecognizedInputFormatException(Exception):
        """
        Exception raised when an input format is specified that is
        not in the VariableInputTypeAdapter.VALID_FORMATS variable.
        """

        def __init__(self, value='The input format was not recognized.'):
            self.value = value

        def __str__(self):
            return repr(self.value)
