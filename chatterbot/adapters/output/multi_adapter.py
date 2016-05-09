from .output_adapter import OutputAdapter


class MultiOutputAdapter(OutputAdapter):

    def __init__(self, **kwargs):
        super(MultiOutputAdapter, self).__init__(**kwargs)

        self.adapters = []

    def add_adapter(self, adapter):
        self.adapters.append(adapter)

    def set_context(self, context):
        """
        Set the context for each of the contained output adapters.
        """
        super(MultiOutputAdapter, self).set_context(context)

        for adapter in self.adapters:
            adapter.set_context(context)

    def process_response(self, statement):
        """
        Takes an input value.
        Returns an output value.
        """
        for i in range(1, len(self.adapters)):
            self.adapters[i].process_response(statement)

        return self.adapters[0].process_response(statement)
