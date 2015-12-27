from .logic import LogicAdapter


class MultiLogicAdapter(LogicAdapter):

    def __init__(self, **kwargs):
        super(MultiLogicAdapter, self).__init__(**kwargs)

        self.adapters = []

    def process(self, statement):
        """
        Returns the outout of a selection of logic adapters
        for a given input statement.
        """
        result = None
        confidence = 0

        for adapter in self.adapters:
            output = adapter.process(statement)
            result = output

        return result #, confidence

    def add_adapter(self, adapter):
        self.adapters.append(adapter)

    def set_context(self, context):
        """
        Set the context for each of the contained logic adapters.
        """
        super(MultiLogicAdapter, self).set_context(context)

        for adapter in self.adapters:
            # TODO, will this actually set the context on the instance?
            adapter.set_context(context)

