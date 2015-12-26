from chatterbot.adapters import Adapter
from chatterbot.adapters.exceptions import AdapterNotImplementedError


class LogicAdapter(Adapter):
    """
    This is an abstract class that represents the interface
    that all logic adapters should implement.
    """

    def process(self, text):
        """
        Method that takes an input statement and returns
        a statement as output.
        """
        raise AdapterNotImplementedError()

