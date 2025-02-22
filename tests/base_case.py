from unittest import TestCase, SkipTest
from chatterbot import ChatBot
from chatterbot.conversation import Statement


class ChatBotTestCase(TestCase):

    def setUp(self):
        self.chatbot = ChatBot('Test Bot', **self.get_kwargs())

    def _add_search_text(self, **kwargs):
        """
        Return the search text for a statement.
        """

        if 'text' in kwargs:
            kwargs['search_text'] = self.chatbot.tagger.get_text_index_string(
                kwargs['text']
            )

        if 'in_response_to' in kwargs:
            kwargs['search_in_response_to'] = self.chatbot.tagger.get_text_index_string(
                kwargs['in_response_to']
            )

        return Statement(**kwargs)

    def _create_with_search_text(self, text, in_response_to=None, **kwargs):
        """
        Helper function to create a statement with the search text populated.
        """
        search_in_response_to = None

        if in_response_to:
            search_in_response_to = self.chatbot.tagger.get_text_index_string(
                in_response_to
            )

        self.chatbot.storage.create(
            text=text,
            in_response_to=in_response_to,
            search_text=self.chatbot.tagger.get_text_index_string(text),
            search_in_response_to=search_in_response_to,
            **kwargs
        )

    def _create_many_with_search_text(self, statements):
        """
        Helper function to bulk-create statements with the search text populated.
        """
        modified_statements = []

        for statement in statements:
            statement.search_text = self.chatbot.tagger.get_text_index_string(
                statement.text
            )

            if statement.in_response_to:
                statement.search_in_response_to = self.chatbot.tagger.get_text_index_string(
                    statement.in_response_to
                )

            modified_statements.append(statement)

        self.chatbot.storage.create_many(statements)

    def tearDown(self):
        """
        Remove the test database.
        """
        self.chatbot.storage.drop()

    def assertIsLength(self, item, length):
        """
        Assert that an iterable has the given length.
        """
        if len(item) != length:
            message = 'Length {} is not equal to {}'.format(len(item), length)
            raise self.failureException(message)

    def get_kwargs(self):
        return {
            # Run the test database in-memory
            'database_uri': None,
            # Don't execute initialization processes such as downloading required data
            'initialize': False
        }


class ChatBotMongoTestCase(ChatBotTestCase):

    @classmethod
    def setUpClass(cls):
        from pymongo.errors import ServerSelectionTimeoutError
        from pymongo import MongoClient

        # Skip these tests if a mongo client is not running
        try:
            client = MongoClient(
                serverSelectionTimeoutMS=0.1
            )
            client.server_info()

        except ServerSelectionTimeoutError:
            raise SkipTest('Unable to connect to Mongo DB.')

    def get_kwargs(self):
        kwargs = super().get_kwargs()
        kwargs['database_uri'] = 'mongodb://localhost:27017/chatterbot_test_database'
        kwargs['storage_adapter'] = 'chatterbot.storage.MongoDatabaseAdapter'
        return kwargs


class ChatBotSQLTestCase(ChatBotTestCase):

    def get_kwargs(self):
        kwargs = super().get_kwargs()
        kwargs['storage_adapter'] = 'chatterbot.storage.SQLStorageAdapter'
        return kwargs
