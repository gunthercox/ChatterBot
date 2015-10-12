from chatterbot.adapters.exceptions import AdapterNotImplementedError


class LogicAdapter(object):
    """
    This is an abstract class that represents the interface
    that all logic adapters should implement.
    """

    def get(self, text, list_of_statements, current_conversation):
        raise AdapterNotImplementedError()

