from chatterbot.adapters import Adapter
from chatterbot.adapters.exceptions import AdapterNotImplementedError


class IOAdapter(Adapter):
    """
    This is an abstract class that represents the interface
    that all IO (input-output) adapters should implement.
    """

    def __init__(self, **kwargs):
        super(IOAdapter, self).__init__(**kwargs)

        # A temporary list of statements that have been processed by an adapter
        self.statement_history = []

    def process_input(self, *args, **kwargs):
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
