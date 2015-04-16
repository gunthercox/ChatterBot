class DatabaseAdapterNotImplementedError(NotImplementedError):
    def __init__(self, message="This method must be overridden in a subclass method."):
        self.message = message


class DatabaseAdapter(object):

    def find(self, key):
        """
        Returns a object from the database if it exists
        """
        except DatabaseAdapterNotImplementedError()

    def insert(self, key):
        """
        Creates a new entry in the database.
        """
        except DatabaseAdapterNotImplementedError()

    def update(self, key):
        """
        Modifies an entry in the database.
        """
        except DatabaseAdapterNotImplementedError()
