from chatterbot.adapters.exceptions import AdapterNotImplementedError


class IOAdapter(object):
    """
    This is an abstract class that represents the interface
    that all input-output adapters should implement.
    """

    def __init__(self, **kwargs):
        pass

    def process_input(self):
        """
        Returns data retrieved from the input source.
        """
        raise AdapterNotImplementedError()

    def process_response(self, input_value):
        """
        Takes an input value.
        Returns an output value.
        """
        raise AdapterNotImplementedError()

