from chatterbot.adapters.storage import DatabaseAdapter
from jsondb.db import Database


class JsonDatabaseAdapter(DatabaseAdapter):

    def __init__(self, database_path):
        self.database = Database(database_path)

    def find(self, key):
        return self.database.data(key=key)

    def insert(self, key, values):
        self.database[key] = values

        return values

    def update(self, key, **kwargs):

        values = self.database.data(key=key)

        # Create the statement if it doesn't exist in the database
        if not values:
            self.database[key] = {}
            values = {}

        for parameter in kwargs:
            values[parameter] = kwargs.get(parameter)

        self.database[key] = values

        return values

    def keys(self):
        # The value has to be cast as a list for Python 3 compatibility
        return list(self.database[0].keys())

    def get_random(self):
        """
        Returns a random statement from the database
        """
        from random import choice

        statement = choice(self.keys())
        return {statement: self.find(statement)}
