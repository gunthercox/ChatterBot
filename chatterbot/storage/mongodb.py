import re
from random import randint
from chatterbot.storage import StorageAdapter


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
        super().__init__(**kwargs)
        from pymongo import MongoClient
        from pymongo.errors import OperationFailure

        self.database_uri = kwargs.get(
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

    def get_statement_model(self):
        """
        Return the class for the statement model.
        """
        from chatterbot.conversation import Statement

        # Create a storage-aware statement
        statement = Statement
        statement.storage = self

        return statement

    def count(self) -> int:
        return self.statements.count_documents({})

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

        page_size = kwargs.pop('page_size', 1000)
        order_by = kwargs.pop('order_by', None)
        tags = kwargs.pop('tags', [])
        exclude_text = kwargs.pop('exclude_text', None)
        exclude_text_words = kwargs.pop('exclude_text_words', [])
        persona_not_startswith = kwargs.pop('persona_not_startswith', None)
        search_text_contains = kwargs.pop('search_text_contains', None)
        search_in_response_to_contains = kwargs.pop('search_in_response_to_contains', None)

        if tags:
            kwargs['tags'] = {
                '$in': tags
            }

        if exclude_text:
            if 'text' not in kwargs:
                kwargs['text'] = {}
            elif 'text' in kwargs and isinstance(kwargs['text'], str):
                text = kwargs.pop('text')
                kwargs['text'] = {
                    '$eq': text
                }
            kwargs['text']['$nin'] = exclude_text

        if exclude_text_words:
            if 'text' not in kwargs:
                kwargs['text'] = {}
            elif 'text' in kwargs and isinstance(kwargs['text'], str):
                text = kwargs.pop('text')
                kwargs['text'] = {
                    '$eq': text
                }
            exclude_word_regex = '|'.join([
                '.*{}.*'.format(word) for word in exclude_text_words
            ])
            kwargs['text']['$not'] = re.compile(exclude_word_regex)

        if persona_not_startswith:
            if 'persona' not in kwargs:
                kwargs['persona'] = {}
            elif 'persona' in kwargs and isinstance(kwargs['persona'], str):
                persona = kwargs.pop('persona')
                kwargs['persona'] = {
                    '$eq': persona
                }
            kwargs['persona']['$not'] = re.compile('^bot:*')

        if search_text_contains:
            or_regex = '|'.join([
                '{}'.format(re.escape(word)) for word in search_text_contains.split(' ')
            ])
            kwargs['search_text'] = re.compile(or_regex)

        if search_in_response_to_contains:
            or_regex = '|'.join([
                '{}'.format(re.escape(word)) for word in search_in_response_to_contains.split(' ')
            ])
            kwargs['search_in_response_to'] = re.compile(or_regex)

        mongo_ordering = []

        if order_by:

            # Sort so that newer datetimes appear first
            if 'created_at' in order_by:
                order_by.remove('created_at')
                mongo_ordering.append(('created_at', pymongo.DESCENDING, ))

            for order in order_by:
                mongo_ordering.append((order, pymongo.ASCENDING))

        total_statements = self.statements.count_documents(kwargs)

        for start_index in range(0, total_statements, page_size):
            if mongo_ordering:
                for match in self.statements.find(kwargs).sort(mongo_ordering).skip(start_index).limit(page_size):
                    yield self.mongo_to_object(match)
            else:
                for match in self.statements.find(kwargs).skip(start_index).limit(page_size):
                    yield self.mongo_to_object(match)

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

    def create_many(self, statements):
        """
        Creates multiple statement entries.
        """
        create_statements = []

        for statement in statements:
            statement_data = statement.serialize()
            tag_data = list(set(statement_data.pop('tags', [])))
            statement_data['tags'] = tag_data

            create_statements.append(statement_data)

        self.statements.insert_many(create_statements)

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

    def drop(self):
        """
        Remove the database.
        """
        self.client.drop_database(self.database.name)
