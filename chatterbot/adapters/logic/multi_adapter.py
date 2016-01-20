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
        max_confidence = -1

        for adapter in self.adapters:
            if adapter.can_process(statement):
                confidence, output = adapter.process(statement)
                if confidence > max_confidence:
                    result = output
                    max_confidence = confidence

        return max_confidence, result

    def add_adapter(self, adapter):
        self.adapters.append(adapter)

    def set_context(self, context):
        """
        Set the context for each of the contained logic adapters.
        """
        super(MultiLogicAdapter, self).set_context(context)

        for adapter in self.adapters:
            adapter.set_context(context)
