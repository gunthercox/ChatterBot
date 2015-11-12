from chatterbot.adapters.exceptions import AdapterNotImplementedError


class PreProcessorAdapter(object):
    """
    This is an abstract class that represents the interface
    that all preprocess adapters should implement.
    """

    def __init__(self, **kwargs):
        pass

    def process(self, text):
        raise AdapterNotImplementedError()
