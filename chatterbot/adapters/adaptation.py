from chatterbot.adapters.exceptions import UnknownAdapterTypeException
from chatterbot.adapters.storage import StorageAdapter
from chatterbot.adapters.logic import LogicAdapter
from chatterbot.adapters.io import IOAdapter
from chatterbot.adapters.logic import MultiLogicAdapter
from chatterbot.adapters.io import MultiIOAdapter
from chatterbot.utils.module_loading import import_module


class Adaptation(object):
    """
    This is a base from which ChatterBot inherits utility methods
    and a context attribute that allows access of adapters to be
    shared between other adapters. This also makes it possible to
    share other context information such as a name, or the current
    conversation with each of the adapters.
    """

    def __init__(self, **kwargs):
        self.storage_adapters = []

        self.io = MultiIOAdapter(**kwargs)

        self.logic = MultiLogicAdapter(**kwargs)
        self.logic.set_context(self)

        # Add required system adapter
        self.add_adapter("chatterbot.adapters.logic.NoKnowledgeAdapter")

    def add_adapter(self, adapter, **kwargs):
        NewAdapter = import_module(adapter)

        adapter = NewAdapter(**kwargs)

        if issubclass(NewAdapter, StorageAdapter):
            self.storage_adapters.append(adapter)
        elif issubclass(NewAdapter, LogicAdapter):
            self.logic.add_adapter(adapter)
        elif issubclass(NewAdapter, IOAdapter):
            self.io.add_adapter(adapter)
        else:
            raise UnknownAdapterTypeException()
