from unittest import TestCase, SkipTest
from chatterbot import ChatBot


class ChatBotTestCase(TestCase):

    def setUp(self):
        self.chatbot = ChatBot('Test Bot', **self.get_kwargs())

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
            raise AssertionError(
                'Length {} is not equal to {}'.format(len(item), length)
            )

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
