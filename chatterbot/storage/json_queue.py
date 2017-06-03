import json
import logging
import queue
import threading
import time
import traceback

from chatterbot.storage import StorageAdapter
from chatterbot.conversation import Response
from datetime import datetime


comptime = '%m %d %Y %H %M %S'

class SafeDatabase(object):
    def __init__(self, filename, auto_start=True, module=json, overwrite=False, interval=0.25):
        self.filename = filename
        self.module = module
        self.overwrite = overwrite
        self.__stop = False

        try:
            self.data = module.load(open(filename))

        except (IOError, ValueError) as err:
            print "Got following error trying to load database, defaulting to {}:"
            traceback.print_exc()
            self.data = {}
            self.write({})

        self.errors = queue.Queue()

        self._loop_thread = threading.Thread(target=self.main_loop, args=(interval,))

        if auto_start:
            self._loop_thread.start()

    def drop(self):
        self.__stop = True

    def run(self):
        self._loop_thread.start()

    def main_loop(self, interval=0.25):
        while not self.__stop:
            if not self.overwrite:
                self.update()

            self.write()

            time.sleep(interval)

    def update(self):
        self.data = self.module.load(open(self.filename))

    def write(self, data=None):
        if not data: data = self.data

        self.fp().write()

    def fp(self):
        while True:
            try:
                return open(self.filename, "w+")

            except (IOError, WindowsError) as err:
                self.errors.put(err)

                time.sleep(0.5)

    def __setitem__(self, key, value):
        self.data[key] = value

    def __getitem__(self, key, safe=True):
        self.update()

        try:
            return self.data[key]

        except KeyError:
            return None

    def keys(self):
        self.update()
        return self.data.keys()

    def values(self):
        self.update()
        return self.data.values()

    def items(self):
        self.update()
        return self.data.items()

    def __len__(self):
        self.update()
        return len(self.data)

    def __delitem__(self, key):
        del self.data[key]

    def delete(self, key):
        del self.data[key]

class SafeJsonFileStorageAdapter(StorageAdapter):
    # Yes, this has some bits from jsonfile.py. Please pardon
    # me. -Gustavo

    def __init__(self, base_query=None, *args, **kwargs):
        """
        Initialize common attributes shared by all storage adapters.
        """
        self.kwargs = kwargs
        self.logger = kwargs.get('logger', logging.getLogger(__name__))
        self.adapter_supports_queries = False
        self.base_query = None

        self.database = SafeDatabase(kwargs.get("database", "database.json"))

    def _keys(self):
        return self.database.keys()

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

        statement_data['created_at'] = datetime.strptime(statement_data['created_at'], comptime)

        return self.Statement(text, **statement_data)

    def count(self):
        """
        Return the number of entries in the database.
        """
        return len(self.database)

    def find(self, statement_text):
        """
        Returns a object from the database if it exists
        """
        values = self.database[statement_text]

        if not values:
            return None

        values['text'] = statement_text

        return self.json_to_object(values)

    def remove(self, statement_text):
        """
        Removes the statement that matches the input text.
        Removes any responses from statements if the response text matches the
        input text.
        """
        for statement in self.filter(in_response_to__contains=statement_text):
            statement.remove_response(statement_text)
            self.update(statement)

        self.database.delete(statement_text)

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

    def get_random(self):
        from random import choice

        if self.count() < 1:
            raise self.EmptyDatabaseException()

        statement = choice(self._keys())
        return self.find(statement)

    def filter(self, **kwargs):
        """
        Returns a list of statements in the database
        that match the parameters specified.
        """
        from operator import attrgetter

        results = []

        order_by = kwargs.pop('order_by', None)

        for key in self._keys():
            values = self.database[key]

            # Add the text attribute to the values
            values['text'] = key

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

        del data['text']
        data['created_at'] = data['created_at'].strftime(comptime)
        self.database[statement.text] = data

        # Make sure that an entry for each response exists
        for response_statement in statement.in_response_to:
            response = self.find(response_statement.text)

            if not response:
                response = self.Statement(response_statement.text)
                self.update(response)

        return statement

    def drop(self):
        """
        Drop the database attached to a given adapter.
        """
        pass

    def get_response_statements(self):
        """
        Return only statements that are in response to another statement.
        A statement must exist which lists the closest matching statement in the
        in_response_to field. Otherwise, the logic adapter may find a closest
        matching statement that does not have a known response.

        This method may be overridden by a child class to provide more a
        efficient method to get these results.
        """
        statement_list = self.filter()

        responses = set()
        to_remove = list()
        for statement in statement_list:
            for response in statement.in_response_to:
                responses.add(response.text)
        for statement in statement_list:
            if statement.text not in responses:
                to_remove.append(statement)

        for statement in to_remove:
            statement_list.remove(statement)

        return statement_list

    class EmptyDatabaseException(Exception):
        def __init__(self, value='The database currently contains no entries. At least one entry is expected. You may need to train your chat bot to populate your database.'):
            self.value = value

        def __str__(self):
            return repr(self.value)
