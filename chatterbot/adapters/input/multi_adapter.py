from .input_adapter import InputAdapter


class MultiInputAdapter(InputAdapter):

    def __init__(self, **kwargs):
        super(MultiInputAdapter, self).__init__(**kwargs)

        self.adapters = []

    def add_adapter(self, adapter):
        self.adapters.append(adapter)

    def set_context(self, context):
        """
        Set the context for each of the contained input adapters.
        """
        super(MultiInputAdapter, self).set_context(context)

        for adapter in self.adapters:
            adapter.set_context(context)

    def process_input(self, *args, **kwargs):
        """
        Returns data retrieved from the input source.
        """
        return self.adapters[0].process_input(*args, **kwargs)
