from chatterbot.adapters import Adapter
from chatterbot.adapters.exceptions import AdapterNotImplementedError


class OutputAdapter(Adapter):
    """
    This is an abstract class that represents the
    interface that all output adapters should implement.
    """

    def process_response(self, input_value):
        """
        Takes an input value.
        Returns an output value.
        """
        raise AdapterNotImplementedError()
