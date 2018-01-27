from unittest import TestCase
from unittest import SkipTest
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
            'input_adapter': 'chatterbot.input.VariableInputTypeAdapter',
            'output_adapter': 'chatterbot.output.OutputAdapter',
            'show_training_progress': False,
            # Run the test database in-memory
            'database': None
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
        kwargs = super(ChatBotMongoTestCase, self).get_kwargs()
        kwargs['database'] = 'chatterbot_test_database'
        kwargs['storage_adapter'] = 'chatterbot.storage.MongoDatabaseAdapter'
        return kwargs


class ChatBotSQLTestCase(ChatBotTestCase):

    def setUp(self):
        """
        Create the tables in the database before each test is run.
        """
        super(ChatBotSQLTestCase, self).setUp()
        self.chatbot.storage.create()

    def get_kwargs(self):
        kwargs = super(ChatBotSQLTestCase, self).get_kwargs()
        del kwargs['database']
        kwargs['storage_adapter'] = 'chatterbot.storage.SQLStorageAdapter'
        return kwargs
