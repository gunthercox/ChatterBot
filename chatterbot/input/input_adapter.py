from chatterbot.adapters import Adapter


class InputAdapter(Adapter):
    """
    This is an abstract class that represents the
    interface that all input adapters should implement.
    """

    def process_input(self, statement):
        """
        Returns a statement object based on the input source.
        """
        raise self.AdapterMethodNotImplementedError()
