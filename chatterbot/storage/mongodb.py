from chatterbot.storage import StorageAdapter


class Query(object):

    def __init__(self, query={}):
        self.query = query

    def value(self):
        return self.query.copy()

    def raw(self, data):
        query = self.query.copy()

        query.update(data)

        return Query(query)

    def statement_text_equals(self, statement_text):
        query = self.query.copy()

        query['text'] = statement_text

        return Query(query)

    def statement_text_not_in(self, statements):
        query = self.query.copy()

        if 'text' not in query:
            query['text'] = {}

        if '$nin' not in query['text']:
            query['text']['$nin'] = []

        query['text']['$nin'].extend(statements)

        return Query(query)

    def statement_response_list_contains(self, statement_text):
        query = self.query.copy()

        if 'in_response_to' not in query:
            query['in_response_to'] = {}

        query['in_response_to']['text'] = statement_text

        return Query(query)

    def statement_response_list_equals(self, response):
        query = self.query.copy()

        query['in_response_to'] = response

        return Query(query)


class MongoDatabaseAdapter(StorageAdapter):
    """
    The MongoDatabaseAdapter is an interface that allows
    ChatterBot to store statements in a MongoDB database.

    :keyword database: The name of the database you wish to connect to.
    :type database: str

    .. code-block:: python

       database='chatterbot-database'

    :keyword database_uri: The URI of a remote instance of MongoDB.
    :type database_uri: str

    .. code-block:: python

       database_uri='mongodb://example.com:8100/'
    """

    def __init__(self, **kwargs):
        super(MongoDatabaseAdapter, self).__init__(**kwargs)
        from pymongo import MongoClient

        self.database_name = self.kwargs.get(
            'database', 'chatterbot-database'
        )
        self.database_uri = self.kwargs.get(
            'database_uri', 'mongodb://localhost:27017/'
        )

        # Use the default host and port
        self.client = MongoClient(self.database_uri)

        # Specify the name of the database
        self.database = self.client[self.database_name]

        self.base_query = Query()

    def count(self):
        return self.database['statements'].count()

    def find(self, statement_text):
        query = self.base_query.statement_text_equals(statement_text)

        values = self.database['statements'].find_one(query.value())

        if not values:
            return None

        del values['text']

        if 'in_response_to' in values:
            values['in_response_to'] = self.deserialize_responses(
                values['in_response_to']
            )

        return self.Statement(statement_text, **values)

    def deserialize_responses(self, statement_data):
        """
        Takes the list of response items and returns
        the list converted to Response objects.
        """
        text = statement_data['text']
        del statement_data['text']

        return self.Statement(text, **statement_data)

    def mongo_to_object(self, object_data):
        """
        Return Statement object when given data
        returned from Mongo DB.
        """
        if 'text' in object_data:
            statement_text = object_data['text']
            del object_data['text']

            if 'in_response_to' in object_data:
                object_data['in_response_to'] = self.deserialize_responses(
                    object_data['in_response_to']
                )

            return self.Statement(statement_text, **object_data)
        else:
            statements = []

            for statement_data in object_data.get('statements'):
                statements.append(self.mongo_to_object(statement_data))

            return self.Conversation(
                id=object_data['id'],
                statements=statements
            )

    def filter(self, obj, **kwargs):
        """
        Returns a list of statements in the database
        that match the parameters specified.
        """
        import pymongo

        query = self.base_query

        order_by = kwargs.pop('order_by', None)

        # Convert response statement objects to data
        if 'in_response_to' in kwargs:
            serialized_response = {'text': kwargs['in_response_to']}

            query = query.statement_response_list_equals(serialized_responses)
            del kwargs['in_response_to']

        if 'in_response_to__contains' in kwargs:
            query = query.statement_response_list_contains(
                kwargs['in_response_to__contains']
            )
            del kwargs['in_response_to__contains']

        query = query.raw(kwargs)

        matches = self.database[obj.collection_name].find(query.value())

        if order_by:

            direction = pymongo.ASCENDING

            # Sort so that newer datetimes appear first
            if order_by == 'created_at':
                direction = pymongo.DESCENDING

            matches = matches.sort(order_by, direction)

        results = []

        for match in list(matches):
            results.append(self.mongo_to_object(match))

        return results

    def update(self, obj):
        from pymongo import UpdateOne
        from pymongo.errors import BulkWriteError

        data = obj.serialize()

        operations = []

        update_operation = UpdateOne(
            {obj.pk_field: getattr(obj, obj.pk_field)},
            {'$set': data},
            upsert=True
        )
        operations.append(update_operation)

        # Make sure that the response is saved
        response_data = data.get('in_response_to', None)

        if response_data:
            update_operation = UpdateOne(
                {'text': response_data['text']},
                {'$set': response_data},
                upsert=True
            )
            operations.append(update_operation)

        try:
            self.database[obj.collection_name].bulk_write(operations, ordered=False)
        except BulkWriteError as bwe:
            # Log the details of a bulk write error
            self.logger.error(str(bwe.details))

        return obj

    def get_random(self):
        """
        Returns a random statement from the database
        """
        from random import randint

        count = self.count()

        if count < 1:
            raise self.EmptyDatabaseException()

        random_integer = randint(0, count - 1)

        statements = self.database['statements'].find().limit(1).skip(random_integer)

        return self.mongo_to_object(list(statements)[0])

    def remove(self, obj):
        """
        Removes the statement that matches the input text.
        Removes any responses from statements if the response text matches the
        input text.
        """
        for statement in self.filter(obj, in_response_to__contains=obj.text):
            statement.remove_response(obj.text)
            self.update(statement)

        self.database[obj.collection_name].delete_one({'text': obj.text})

    def get_response_statements(self):
        """
        Return only statements that are in response to another statement.
        A statement must exist which lists the closest matching statement in the
        in_response_to field. Otherwise, the logic adapter may find a closest
        matching statement that does not have a known response.
        """
        statements = self.database['statements']
        response_query = statements.distinct('in_response_to.text')

        _statement_query = {
            'text': {
                '$in': response_query
            }
        }

        _statement_query.update(self.base_query.value())

        statement_query = statements.find(_statement_query)

        statement_objects = []

        for statement in list(statement_query):
            statement_objects.append(self.mongo_to_object(statement))

        return statement_objects

    def drop(self):
        """
        Remove the database.
        """
        self.client.drop_database(self.database_name)
