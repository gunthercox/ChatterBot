from chatterbot.utils.module_loading import import_module


class Adaptation(object):

    class context(object):
        data = {}

        def __getattr__(self, key):
            return getattr(data, key)

        def __setattr__(self, key, value):
            return setattr(data, key, value)

    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def add_adapter(self, name, adapter):
        NewAdapter = import_module(adapter)
        self.context.data[name] = NewAdapter(self.context, **self.kwargs)

        return self.context.data[name]

