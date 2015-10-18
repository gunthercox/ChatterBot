from chatterbot.adapters.exceptions import AdapterNotImplementedError


class LogicAdapter(object):
    """
    This is an abstract class that represents the interface
    that all logic adapters should implement.
    """

    def __init__(self, **kwargs):
        pass

    def get(self, text, statement_list, current_conversation):
        raise AdapterNotImplementedError()

