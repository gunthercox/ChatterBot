from chatterbot.adapters.storage import DatabaseAdapter
from pymongo import MongoClient

# Use the default host and port
client = MongoClient()

# We can also specify the host and port explicitly
#client = MongoClient('localhost', 27017)

# Specify the name of the database
db = client['test-database']

# The mongo collection of statement documents
statements = db['statements']


class MongoDatabaseAdapter(DatabaseAdapter):

    def __init__(self, **kwargs):
        pass

    def find(self, statement):
    #def find(self, key):
        return statements.find_one(statement)

    def insert(self, key, values):
        statement_id = self.statements.insert_one(statement).inserted_id

        return statement_id

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
