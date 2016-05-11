class Adapter(object):
    """
    An abstract superclass for all adapters
    """

    def __init__(self, **kwargs):
        self.context = None

    def set_context(self, context):
        self.context = context

    class AdapterMethodNotImplementedError(NotImplementedError):

        def __init__(self, message="This method must be overridden in a subclass method."):
            self.message = message

        def __str__(self):
            return self.message
