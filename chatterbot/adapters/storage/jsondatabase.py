from chatterbot.adapters.storage import DatabaseAdapter
from chatterbot.adapters.exceptions import EmptyDatabaseException
from chatterbot.conversation import Statement
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

    def find(self, statement_text):
        values = self.database.data(key=statement_text)

        if not values:
            return None

        return Statement(statement_text, **values)

    def _all_kwargs_match_values(self, kwarguments, values):

        for kwarg in kwarguments:

            if "__" in kwarg:
                kwarg_parts = kwarg.split("__")

                if kwarg_parts[1] == "contains":
                    if kwarguments[kwarg] not in values[kwarg_parts[0]]:
                        return False

            if kwarg in values:
                if values[kwarg] != kwarguments[kwarg]:
                    return False

        return True

    def filter(self, **kwargs):
        """
        Returns a list of statements in the database
        that match the parameters specified.
        """
        results = []

        for key in self._keys():
            values = self.database.data(key=key)

            if self._all_kwargs_match_values(kwargs, values):
                results.append(
                    Statement(key, **values)
                )

        return results

    def update(self, statement):
        # Do not alter the database unless writing is enabled
        if not self.read_only:
            data = statement.serialize()

            # Remove the text key from the data
            del(data['text'])
            self.database[statement.text] = data

            # Make sure that an entry for each response is saved
            for response_statement in statement.in_response_to:
                response = self.find(response_statement)
                if not response:
                    response = Statement(response_statement)
                    self.update(response)

        return statement

    def get_random(self):
        from random import choice

        if self.count() < 1:
            raise EmptyDatabaseException()

        statement = choice(self._keys())
        return self.find(statement)

    def drop(self):
        """
        Remove the json file database completely.
        """
        import os

        os.remove(self.database.path)

