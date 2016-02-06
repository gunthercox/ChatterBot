from chatterbot.adapters import Adapter
from chatterbot.adapters.exceptions import AdapterNotImplementedError


class StorageAdapter(Adapter):
    """
    This is an abstract class that represents the interface
    that all storage adapters should implement.
    """

    def __init__(self, **kwargs):
        super(StorageAdapter, self).__init__(**kwargs)

        self.kwargs = kwargs
        self.read_only = kwargs.get("read_only", False)

    def count(self):
        """
        Return the number of entries in the database.
        """
        raise AdapterNotImplementedError()

    def find(self, statement_text):
        """
        Returns a object from the database if it exists
        """
        raise AdapterNotImplementedError()

    def remove(self, statement_text):
        """
        Removes the statement that matches the input text.
        Removes any responses from statements where the response text matches
        the input text.
        """
        raise AdapterNotImplementedError()

    def filter(self, **kwargs):
        """
        Returns a list of objects from the database.
        The kwargs parameter can contain any number
        of attributes. Only objects which contain
        all listed attributes and in which all values
        match for all listed attributes will be returned.
        """
        raise AdapterNotImplementedError()

    def update(self, statement):
        """
        Modifies an entry in the database.
        Creates an entry if one does not exist.
        """
        raise AdapterNotImplementedError()

    def get_random(self):
        """
        Returns a random statement from the database
        """
        raise AdapterNotImplementedError()

    def drop(self):
        """
        Drop the database attached to a given adapter.
        """
        raise AdapterNotImplementedError()
