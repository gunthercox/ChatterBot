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

    def statement_in_response_to_not_in(self, statements):
        query = self.query.copy()

        if 'in_response_to' not in query:
            query['in_response_to'] = {}

        if '$nin' not in query['in_response_to']:
            query['in_response_to']['$nin'] = statements

        return Query(query)


class MongoDatabaseAdapter(StorageAdapter):
    """
    The MongoDatabaseAdapter is an interface that allows
    ChatterBot to store statements in a MongoDB database.

    :keyword database_uri: The URI of a remote instance of MongoDB.
                           This can be any valid
                           `MongoDB connection string <https://docs.mongodb.com/manual/reference/connection-string/>`_
    :type database_uri: str

    .. code-block:: python

       database_uri='mongodb://example.com:8100/'
    """

    def __init__(self, **kwargs):
        super(MongoDatabaseAdapter, self).__init__(**kwargs)
        from pymongo import MongoClient
        from pymongo.errors import OperationFailure

        self.database_uri = self.kwargs.get(
            'database_uri', 'mongodb://localhost:27017/chatterbot-database'
        )

        # Use the default host and port
        self.client = MongoClient(self.database_uri)

        # Increase the sort buffer to 42M if possible
        try:
            self.client.admin.command({'setParameter': 1, 'internalQueryExecMaxBlockingSortBytes': 44040192})
        except OperationFailure:
            pass

        # Specify the name of the database
        self.database = self.client.get_database()

        # The mongo collection of statement documents
        self.statements = self.database['statements']

        self.base_query = Query()

    def get_statement_model(self):
        """
        Return the class for the statement model.
        """
        from chatterbot.conversation import Statement

        # Create a storage-aware statement
        statement = Statement
        statement.storage = self

        return statement

    def count(self):
        return self.statements.count()

    def mongo_to_object(self, statement_data):
        """
        Return Statement object when given data
        returned from Mongo DB.
        """
        Statement = self.get_model('statement')

        statement_data['id'] = statement_data['_id']

        return Statement(**statement_data)

    def filter(self, **kwargs):
        """
        Returns a list of statements in the database
        that match the parameters specified.
        """
        import pymongo

        query = self.base_query

        order_by = kwargs.pop('order_by', None)

        query = query.raw(kwargs)

        matches = self.statements.find(query.value())

        if order_by:

            mongo_ordering = []

            # Sort so that newer datetimes appear first
            if 'created_at' in order_by:
                order_by.remove('created_at')
                mongo_ordering.append(('created_at', pymongo.DESCENDING, ))

            for order in order_by:
                mongo_ordering.append((order, pymongo.ASCENDING))

            matches = matches.sort(mongo_ordering)

        results = []

        for match in list(matches):
            results.append(self.mongo_to_object(match))

        return results

    def create(self, **kwargs):
        """
        Creates a new statement matching the keyword arguments specified.
        Returns the created statement.
        """
        Statement = self.get_model('statement')

        if 'tags' in kwargs:
            kwargs['tags'] = list(set(kwargs['tags']))

        inserted = self.statements.insert_one(kwargs)

        kwargs['id'] = inserted.inserted_id

        return Statement(**kwargs)

    def update(self, statement):
        data = statement.serialize()
        data.pop('id', None)
        data.pop('tags', None)

        update_data = {
            '$set': data
        }

        if statement.tags:
            update_data['$addToSet'] = {
                'tags': {
                    '$each': statement.tags
                }
            }

        search_parameters = {}

        if statement.id is not None:
            search_parameters['_id'] = statement.id
        else:
            search_parameters['text'] = statement.text
            search_parameters['conversation'] = statement.conversation

        update_operation = self.statements.update_one(
            search_parameters,
            update_data,
            upsert=True
        )

        if update_operation.acknowledged:
            statement.id = update_operation.upserted_id

        return statement

    def get_random(self):
        """
        Returns a random statement from the database
        """
        from random import randint

        count = self.count()

        if count < 1:
            raise self.EmptyDatabaseException()

        random_integer = randint(0, count - 1)

        statements = self.statements.find().limit(1).skip(random_integer)

        return self.mongo_to_object(list(statements)[0])

    def remove(self, statement_text):
        """
        Removes the statement that matches the input text.
        """
        self.statements.delete_one({'text': statement_text})

    def get_response_statements(self):
        """
        Return only statements that are in response to another statement.
        A statement must exist which lists the closest matching statement in the
        in_response_to field. Otherwise, the logic adapter may find a closest
        matching statement that does not have a known response.
        """
        _response_query = {
            'in_response_to': {
                '$ne': None
            }
        }

        response_query = self.statements.find(_response_query)

        responses = []
        for r in response_query:
            try:
                responses.append(r['in_response_to'])
            except TypeError:
                pass

        _statement_query = {
            'text': {
                '$in': responses
            }
        }

        _statement_query.update(self.base_query.value())
        statement_query = self.statements.find(_statement_query)
        statement_objects = []
        for statement in list(statement_query):
            statement_objects.append(self.mongo_to_object(statement))
        return statement_objects

    def drop(self):
        """
        Remove the database.
        """
        self.client.drop_database(self.database.name)
