from chatterbot.adapters.database import DatabaseAdapter
from jsondb.db import Database


class JsonDatabaseAdapter(DatabaseAdapter):

    def __init__(self, database_path):

        self.database = Database(database)

    def find(self, key):
        pass

    def insert(self, key):
        pass

    def update(self, key):
        pass

    def upsert(self, data):
        pass
