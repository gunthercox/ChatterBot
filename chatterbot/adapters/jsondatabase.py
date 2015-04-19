from chatterbot.adapters.database import DatabaseAdapter
from jsondb.db import Database


class JsonDatabaseAdapter(DatabaseAdapter):

    def __init__(self, database_path):
        self.database = Database(database_path)

    def find(self, key):
        return self.database[key]

    def insert(self, key, values):
        self.database[key] = values

    def update(self, key, values):
        self.database[key] = values

    def keys(self):
        # The return value has to be cast as a list for Python 3 compatibility
        return list(self.database[0].keys())

    def get_random(self):
        """
        Returns a random statement from the database
        """
        from random import choice
        return choice(self.keys())
