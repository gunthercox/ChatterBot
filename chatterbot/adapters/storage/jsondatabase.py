from chatterbot.adapters.storage import StorageAdapter
from chatterbot.adapters.exceptions import EmptyDatabaseException
from chatterbot.conversation import Statement, Response
from jsondb import Database


class JsonDatabaseAdapter(StorageAdapter):
    """
    The JsonDatabaseAdapter is an interface that allows ChatterBot
    to store the conversation as a Json-encoded file.
    """

    def __init__(self, **kwargs):
        super(JsonDatabaseAdapter, self).__init__(**kwargs)

        database_path = self.kwargs.get("database", "database.db")
        if self.kwargs.get("database_dir") is not None:
            database_path = self.kwargs.get("database_dir") + self.kwargs.get("database", "database.db")

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
        response_list = self.deserialize_responses(values["in_response_to"])
        values["in_response_to"] = response_list

        return Statement(statement_text, **values)

    def deserialize_responses(self, response_list):
        """
        Takes the list of response items and returns the
        list converted to object versions of the responses.
        """
        in_response_to = []

        for response in response_list:
            text = response["text"]
            del(response["text"])

            in_response_to.append(
                Response(text, **response)
            )

        return in_response_to

    def _all_kwargs_match_values(self, kwarguments, values):
        for kwarg in kwarguments:

            if "__" in kwarg:
                kwarg_parts = kwarg.split("__")

                key = kwarg_parts[0]
                identifier = kwarg_parts[1]

                if identifier == "contains":
                    text_values = []
                    for val in values[key]:
                        text_values.append(val["text"])

                    if (kwarguments[kwarg] not in text_values) and (
                            kwarguments[kwarg] not in values[key]):
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

            # Add the text attribute to the values
            values["text"] = key

            if self._all_kwargs_match_values(kwargs, values):

                # Build the objects for the response list
                in_response_to = values["in_response_to"]
                response_list = self.deserialize_responses(in_response_to)
                values["in_response_to"] = response_list

                # Remove the text attribute from the values
                text = values.pop("text")

                results.append(
                    Statement(text, **values)
                )

        return results

    def update(self, statement):
        # Do not alter the database unless writing is enabled
        if not self.read_only:
            data = statement.serialize()

            # Remove the text key from the data
            del(data['text'])
            self.database.data(key=statement.text, value=data)

            # Make sure that an entry for each response exists
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

        if os.path.exists(self.database.path):
            os.remove(self.database.path)
