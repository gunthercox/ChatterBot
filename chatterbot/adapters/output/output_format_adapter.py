from chatterbot.adapters.output import OutputAdapter
from chatterbot.utils.read_input import input_function


JSON = 'json'
TEXT = 'text'
OBJECT = 'object'
VALID_FORMATS = (JSON, TEXT, OBJECT, )


class OutputFormatAdapter(OutputAdapter):

    def __init__(self, *args, **kwargs):
        super(OutputFormatAdapter, self).__init__(**kwargs)
        self.format = kwargs.get('output_format', 'object')

        if self.format not in VALID_FORMATS:
            raise self.UnrecognizedOutputFormatException(
                'The output type {} is not a known valid format'.format(
                    self.format
                )
            )

    def process_response(self, statement):
        if self.format == TEXT:
            return statement.text

        if self.format == JSON:
            return statement.serialize()

        # Return the statement OBJECT by default
        return statement

    class UnrecognizedOutputFormatException(Exception):
        def __init__(self, message='The input format was not recognized.'):
            super(
                OutputFormatAdapter.UnrecognizedOutputFormatException,
                self
            ).__init__(message)

        def __str__(self):
            return self.message
