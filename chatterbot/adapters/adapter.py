class Adapter(object):

    def __init__(self, **kwargs):
        self.context = None

    def set_context(self, context):
        self.context = context

