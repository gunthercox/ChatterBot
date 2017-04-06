import os.path

from chatterbot.storage import StorageAdapter
from chatterbot.conversation import Response
from chatterbot import utils

class CustomJsonFileStorageAdapter(StorageAdapter):
    """
    This adapter allows ChatterBot to store conversation
    data in a file in JSON format using custom methods.

    :keyword database: The path to the json file you wish to store data in.
    :type database: str

    :keyword load_func: Dotted path with the load function added.

    :keyword dump_func: Dotted path with the dump function added.
    """

    def __init__(self, **kwargs):
        super(CustomJsonFileStorageAdapter, self).__init__(**kwargs)

        database_path = self.kwargs.get('database', 'database.db')

        load_settings = self.kwargs.get("loads_func", "json.loads")
        dump_settings = self.kwargs.get("dumps_func", "json.dumps")

        self.load = utils.import_module(load_settings)

        self.dump = utils.import_module(dump_settings)

        if not os.path.isfile(database_path):
            self.database = {}
            with open(database_path, "w") as f:
                f.write("{}")

        else:
            with open(database_path) as f:
                self.database = self.load(f.read())

        self._db_path = database_path
        self.adapter_supports_queries = False
        
    def _save(self):
        try:
            # ujson is able to properly save and load datetime objects
            data = self.dump(self.database)
        except TypeError:
            # builtin json isn't
            data = self.dump(self.database, default=lambda o: getattr(o,'__dict__',str(o)))
        with open(self._db_path, "w") as f:
            f.write(data)

    def _keys(self):
        # The value has to be cast as a list for Python 3 compatibility
        return list(self.database.keys())

    def count(self):
        return len(self._keys())

    def find(self, statement_text):
        entry = self.database.get(statement_text)

        if entry is None:
            self.database[statement_text] = {}
            return None
            
        if not entry:
            return None

        entry['text'] = statement_text

        return self.json_to_object(entry)

    def remove(self, statement_text):
        """
        Removes the statement that matches the input text.
        Removes any responses from statements if the response text matches the
        input text.
        """
        for statement in self.filter(in_response_to__contains=statement_text):
            statement.remove_response(statement_text)
            self.update(statement)

        del self.database[statement_text]
        self._save()

    def deserialize_responses(self, response_list):
        """
        Takes the list of response items and returns
        the list converted to Response objects.
        """
        proxy_statement = self.Statement('')

        for response in response_list:
            data = response.copy()
            text = data['text']
            del data['text']

            proxy_statement.add_response(
                Response(text, **data)
            )

        return proxy_statement.in_response_to

    def json_to_object(self, statement_data):
        """
        Converts a dictionary-like object to a Statement object.
        """

        # Don't modify the referenced object
        statement_data = statement_data.copy()

        # Build the objects for the response list
        statement_data['in_response_to'] = self.deserialize_responses(
            statement_data['in_response_to']
        )

        # Remove the text attribute from the values
        text = statement_data.pop('text')

        return self.Statement(text, **statement_data)

    def _all_kwargs_match_values(self, kwarguments, values):
        for kwarg in kwarguments:

            if '__' in kwarg:
                kwarg_parts = kwarg.split('__')

                key = kwarg_parts[0]
                identifier = kwarg_parts[1]

                if identifier == 'contains':
                    text_values = []
                    for val in values[key]:
                        text_values.append(val['text'])

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
        from operator import attrgetter

        results = []

        order_by = kwargs.pop('order_by', None)

        for key in self._keys():
            values = self.database.get(key)
            if values is None:
                self.database["key"] = {}
                values = {}
                continue

            # Add the text attribute to the values
            values['text'] = key
            if not 'in_response_to' in values:
                values['in_response_to'] = []

            if self._all_kwargs_match_values(kwargs, values):
                results.append(self.json_to_object(values))

        if order_by:

            # Sort so that newer datetimes appear first
            is_reverse = order_by == 'created_at'

            # Do an in place sort of the results
            results.sort(key=attrgetter(order_by), reverse=is_reverse)

        return results

    def update(self, statement):
        """
        Update a statement in the database.
        """
        data = statement.serialize()

        # Remove the text key from the data
        del data['text']
        self.database[statement.text] = data

        # Make sure that an entry for each response exists
        for response_statement in statement.in_response_to:
            response = self.find(response_statement.text)
            if not response:
                response = self.Statement(response_statement.text)
                self.update(response)

        return statement

    def get_random(self):
        from random import choice

        if self.count() < 1:
            raise self.EmptyDatabaseException()

        statement = choice(self._keys())
        return self.find(statement)

    def drop(self):
        """
        Remove the json file database completely.
        """
        self.database = {}
        open(self._db_path, "w").close()
