from chatterbot.adapters.output import OutputAdapter
from chatterbot.utils.read_input import input_function


class OutputFormatAdapter(OutputAdapter):

    JSON = 'json'
    TEXT = 'text'
    OBJECT = 'object'
    VALID_FORMATS = (JSON, TEXT, OBJECT, )

    def __init__(self, *args, **kwargs):
        super(OutputFormatAdapter, self).__init__(**kwargs)
        self.format = kwargs.get('output_format', 'object')

        if self.format not in self.VALID_FORMATS:
            raise self.UnrecognizedOutputFormatException(
                'The output type {} is not a known valid format'.format(
                    self.format
                )
            )

    def process_response(self, statement):
        if self.format == self.TEXT:
            return statement.text

        if self.format == self.JSON:
            return statement.serialize()

        # Return the statement OBJECT by default
        return statement

    class UnrecognizedOutputFormatException(Exception):
        """
        A exception raised when the output format specified is not one of the
        options listed in the OutputFormatAdapter.VALID_FORMATS variable.
        """

        def __init__(self, value='The input format was not recognized.'):
            self.value = value

        def __str__(self):
            return repr(self.value)
