import warnings
from chatterbot.storage import StorageAdapter


class JsonFileStorageAdapter(StorageAdapter):
    """
    This adapter allows ChatterBot to store conversation
    data in a file in JSON format.

    :keyword database: The path to the json file you wish to store data in.
    :type database: str

    :keyword silence_performance_warning: If set to True, the :code:`UnsuitableForProductionWarning`
                                          will not be displayed.
    :type silence_performance_warning: bool
    """

    def __init__(self, **kwargs):
        super(JsonFileStorageAdapter, self).__init__(**kwargs)
        import os
        from jsondb import Database

        if not kwargs.get('silence_performance_warning', False):
            warnings.warn(
                'The JsonFileStorageAdapter is not recommended for production environments.',
                self.UnsuitableForProductionWarning
            )

        statement_database_path = self.kwargs.get('database', 'database.db')
        conversation_database_path = 'conversations.db'
        self.database = {
            'statements': Database(statement_database_path),
            'conversations': Database(conversation_database_path)
        }

        # Create the statements document as an empty list
        # self.database['statements'] = []

    def count(self):
        return len(self.database['statements'].keys())

    def find(self, statement_text):
        values = self.database['statements'].data(key=statement_text)

        if not values:
            return None

        values['text'] = statement_text

        return self.json_to_object(values)

    def remove(self, obj):
        """
        Removes the statement that matches the input text.
        Removes any responses from statements if the response text matches the
        input text.
        """
        for statement in self.filter(obj, in_response_to__contains=obj.text):
            statement.remove_response(obj.text)
            self.update(statement)

        self.database['statements'].delete(obj.text)

    def json_to_object(self, object_data):
        """
        Converts a dictionary-like object to a Statement object.
        """

        # Don't modify the referenced object
        object_data = object_data.copy()

        if 'text' in object_data:

            # Build the objects for the response list
            object_data['in_response_to'] = self.Statement(
                **object_data['in_response_to']
            )

            # Remove the text attribute from the values
            text = object_data.pop('text')

            return self.Statement(text, **object_data)
        else:
            statements = []

            for statement_data in object_data['statements']:
                text = statement_data.pop('text')
                statements.append(self.Statement(text, **statement_data))

            return self.Conversation(
                id=object_data['id'],
                statements=statements
            )

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

    def filter(self, obj, **kwargs):
        """
        Returns a list of statements in the database
        that match the parameters specified.
        """
        from operator import attrgetter

        results = []

        order_by = kwargs.pop('order_by', None)

        for statement in self.database['statements']:

            if self._all_kwargs_match_values(kwargs, statement):
                results.append(self.json_to_object(statement))

        if order_by:

            # Sort so that newer datetimes appear first
            is_reverse = order_by == 'created_at'

            # Do an in place sort of the results
            results.sort(key=attrgetter(order_by), reverse=is_reverse)

        return results

    def update(self, obj):
        """
        Update the object in the database.
        """
        data = obj.serialize()

        if 'text' in data:
            statements = self.database['statements']
            statements.append(statement.serialize())

            self.database.data(key='statements', value=statements)
        else:
            del data['id']
            self.database['conversations'].data(key=obj.id, value=data)

        return obj

    def get_random(self):
        from random import choice

        if self.count() < 1:
            raise self.EmptyDatabaseException()

        return choice(self.database['statements'])

    def drop(self):
        """
        Remove the json file database completely.
        """
        self.database['statements'].drop()
        self.database['conversations'].drop()

    class UnsuitableForProductionWarning(Warning):
        """
        The json file storage adapter will display an :code:`UnsuitableForProductionWarning`
        when it is initialized because it is not intended for use in large scale production
        applications. You can silence this warning by setting
        :code:`silence_performance_warning=True` when initializing the adapter.
        """
        pass
