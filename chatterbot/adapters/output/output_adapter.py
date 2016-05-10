from chatterbot.adapters import Adapter


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
        raise self.AdapterMethodNotImplementedError()
