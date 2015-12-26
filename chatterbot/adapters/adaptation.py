from chatterbot.utils.module_loading import import_module


class Adaptation(object):
    """
    This is a base from which ChatterBot inherits utility methods
    and a context attribute that allows access of adapters to be
    shared between other adapters. This also makes it possible to
    share other context information such as a name, or the current
    conversation with each of the adapters.
    """

    class context(object):
        """
        This subclass provides static access to the context data.
        """
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

