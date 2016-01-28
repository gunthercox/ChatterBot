class Adapter(object):
    """
    An abstract superclass for all adapters
    """

    def __init__(self, **kwargs):
        self.context = None

    def set_context(self, context):
        self.context = context
