from chatterbot.adapters.storage import DatabaseAdapter
from chatterbot.adapters.exceptions import EmptyDatabaseException
from jsondb.db import Database


class JsonDatabaseAdapter(DatabaseAdapter):

    def __init__(self, **kwargs):
        super(JsonDatabaseAdapter, self).__init__(**kwargs)
        database_path = self.kwargs.get("database", "database.db")
        self.database = Database(database_path)

    def _keys(self):
        # The value has to be cast as a list for Python 3 compatibility
        return list(self.database[0].keys())

    def count(self):
        return len(self._keys())

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

    def get_random(self):
        from random import choice

        if self.count() < 1:
            raise EmptyDatabaseException()

        statement = choice(self._keys())
        return {statement: self.find(statement)}

    def drop(self):
        """
        Remove the json file database completely
        """
        import os

        os.remove(self.database.path)
