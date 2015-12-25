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

        adapter = NewAdapter(self.context, **self.kwargs)
        setattr(self.context, name, adapter)

        return adapter

