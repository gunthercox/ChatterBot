from chatterbot.adapters import Adapter
from chatterbot.conversation import Statement


class InputAdapter(Adapter):
    """
    This is an abstract class that represents the
    interface that all input adapters should implement.
    """

    DICT = 'json'
    TEXT = 'text'
    OBJECT = 'object'
    VALID_FORMATS = (DICT, TEXT, OBJECT, )

    def detect_type(self, statement):
        if hasattr(statement, 'text'):
            return self.OBJECT
        if isinstance(statement, str):
            return self.TEXT
        if isinstance(statement, dict):
            return self.DICT

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
            return Statement(text=statement)

        # Convert input dictionary into a statement object
        if input_type == self.DICT:
            return Statement(**statement)

    class UnrecognizedInputFormatException(Exception):
        """
        Exception raised when an input format is specified
        that is not in the InputAdapter.VALID_FORMATS variable.
        """

        def __init__(self, message='The input format was not recognized.'):
            super().__init__(message)
