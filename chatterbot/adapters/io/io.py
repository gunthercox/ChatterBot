from chatterbot.adapters.exceptions import AdapterNotImplementedError


class IOAdapter(object):
    """
    This is an abstract class that represents the interface
    that all input-output adapters should implement.
    """

    def process_response(self, input_value):
        """
        Takes an input value.
        Returns an output value.
        """
        raise AdapterNotImplementedError()

