from __future__ import unicode_literals
import warnings
from .output_adapter import OutputAdapter


class OutputFormatAdapter(OutputAdapter):
    """
    Return output from the bot in a specified format.
    """

    JSON = 'json'
    TEXT = 'text'
    OBJECT = 'object'
    VALID_FORMATS = (JSON, TEXT, OBJECT, )

    def __init__(self, *args, **kwargs):
        """
        Set the output format for this adapter.
        """
        super(OutputFormatAdapter, self).__init__(**kwargs)
        self.format = kwargs.get('output_format', 'object')

        if self.format == self.TEXT:
            warnings.warn(
                'OutputFormatAdapter is deprecated. Use OutputAdapter instead and get `.text` from the returned object.',
                DeprecationWarning
            )
        elif self.format == self.JSON:
            warnings.warn(
                'OutputFormatAdapter is deprecated. Use OutputAdapter instead and call `.serialize()` from the returned object.',
                DeprecationWarning
            )
        elif self.format == self.OBJECT:
            warnings.warn(
                'OutputFormatAdapter is deprecated. Use OutputAdapter instead.',
                DeprecationWarning
            )
        elif self.format not in self.VALID_FORMATS:
            raise self.UnrecognizedOutputFormatException(
                'The output type {} is not a known valid format'.format(
                    self.format
                )
            )

    def process_response(self, statement, confidence=None, session_id=None):
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
