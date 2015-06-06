from .logic import LogicAdapter

class ClosestMatchAdapter(LogicAdapter):

    def __init__(self, storage_adapter):
        """
        Constructor takes a statement that exists within
        the database, and the database object.
        """

        self.storage_adapter = storage_adapter

    def get(self, text):
        """
        Takes a statement from the current conversation and a database instance.
        Returns the closest known statement that matches by string comparison.
        """
        from fuzzywuzzy import process

        # Check if an exact match exists
        if self.storage_adapter.find(text):
            return text

        # TODO: The call to the hidden _keys method should not be made here

        # Get the closest matching statement from the database
        return process.extract(text, self.storage_adapter._keys(), limit=1)[0][0]
