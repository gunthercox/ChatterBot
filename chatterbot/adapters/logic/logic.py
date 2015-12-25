from chatterbot.adapters import Adapter
from chatterbot.adapters.exceptions import AdapterNotImplementedError


class LogicAdapter(Adapter):
    """
    This is an abstract class that represents the interface
    that all logic adapters should implement.
    """

    def get(self, text, statement_list, current_conversation):
        raise AdapterNotImplementedError()

