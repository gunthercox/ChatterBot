import logging


class Adapter(object):
    """
    A superclass for all adapter classes.
    """

    def __init__(self, **kwargs):
        self.logger = kwargs.get('logger', logging.getLogger(__name__))
        self.context = None

    def set_context(self, context):
        self.context = context

    class AdapterMethodNotImplementedError(NotImplementedError):

        def __init__(self, message="This method must be overridden in a subclass method."):
            self.message = message

        def __str__(self):
            return self.message
