from chatterbot.adapters.exceptions import AdapterNotImplementedError


class DatabaseAdapter(object):

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
        """
        raise AdapterNotImplementedError()
