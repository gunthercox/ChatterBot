from chatterbot.adapters.exceptions import AdapterNotImplementedError


class DatabaseAdapter(object):

    def __init__(self, **kwargs):
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

