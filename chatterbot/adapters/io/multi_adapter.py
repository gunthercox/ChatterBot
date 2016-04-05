from .io import IOAdapter


class MultiIOAdapter(IOAdapter):

    def __init__(self, **kwargs):
        super(MultiIOAdapter, self).__init__(**kwargs)

        self.adapters = []

    def process_input(self, *args, **kwargs):
        """
        Returns data retrieved from the input source.
        """
        if self.adapters is not []:
            return self.adapters[0].process_input(*args, **kwargs)

    def process_response(self, statement):
        """
        Takes an input value.
        Returns an output value.
        """
        for i in range(1, len(self.adapters)):
            self.adapters[i].process_response(statement)

        return self.adapters[0].process_response(statement)

    def add_adapter(self, adapter):
        self.adapters.append(adapter)

    def set_context(self, context):
        """
        Set the context for each of the contained io adapters.
        """
        super(MultiIOAdapter, self).set_context(context)

        for adapter in self.adapters:
            adapter.set_context(context)
