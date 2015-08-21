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

    def find(self, key):
        """
        Returns a object from the database if it exists
        """
        raise AdapterNotImplementedError()

    def insert(self, key):
        """
        Creates a new entry in the database.
        """
        raise AdapterNotImplementedError()

    def update(self, key):
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
