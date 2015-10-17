from chatterbot.adapters.storage import StorageAdapter
from chatterbot.adapters.exceptions import EmptyDatabaseException
from chatterbot.conversation import Statement, Response
from jsondb import Database


class JsonDatabaseAdapter(StorageAdapter):

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

        # Build the objects for the response list
        response_list = self._objectify_response_list(values["in_response_to"])
        values["in_response_to"] = response_list

        return Statement(statement_text, **values)

    def _objectify_response_list(self, response_list):
        """
        Takes the list of response items and returns a
        the list converted to object versions of the responses.
        """
        in_response_to = []

        for item in response_list:
            text = item[0]
            occurrence = item[1]

            in_response_to.append(
                Response(text, occurrence=occurrence)
            )

        return in_response_to

    def _all_kwargs_match_values(self, kwarguments, values):

        for kwarg in kwarguments:

            if "__" in kwarg:
                kwarg_parts = kwarg.split("__")

                if kwarg_parts[1] == "contains":
                    text_values = []
                    for val in values[kwarg_parts[0]]:
                        text_values.append(val[0])

                    if (kwarguments[kwarg] not in text_values) and (kwarguments[kwarg] not in values[kwarg_parts[0]]):
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

                # Build the objects for the response list
                response_list = self._objectify_response_list(values["in_response_to"])
                values["in_response_to"] = response_list

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
            self.database.data(key=statement.text, value=data)

            # Make sure that an entry for each response is saved
            for response_statement in statement.in_response_to:
                response = self.find(response_statement.text)
                if not response:
                    response = Statement(response_statement.text)
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

