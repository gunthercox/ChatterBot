from chatterbot.adapters.exceptions import AdapterNotImplementedError


class PluginAdapter(object):
    """
    This is an abstract class that represents the interface
    that all plugins should implement.
    """

    def __init__(self, **kwargs):
        pass

    def process(self, text):
        raise AdapterNotImplementedError()

    def should_answer(self, text):
        raise AdapterNotImplementedError()
