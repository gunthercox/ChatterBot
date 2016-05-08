from chatterbot.adapters import Adapter
from chatterbot.adapters.exceptions import AdapterNotImplementedError


class InputAdapter(Adapter):
    """
    This is an abstract class that represents the
    interface that all input adapters should implement.
    """

    def process_input(self, *args, **kwargs):
        """
        Returns data retrieved from the input source.
        """
        raise AdapterNotImplementedError()
