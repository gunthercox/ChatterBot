from unittest import TestCase
from unittest import SkipTest
from chatterbot import ChatBot
import os


class ChatBotTestCase(TestCase):

    def setUp(self):
        self.chatbot = ChatBot('Test Bot', **self.get_kwargs())

    def get_kwargs(self):
        return {
                'input_adapter': {'input_class': 'chatterbot.adapters.input.VariableInputTypeAdapter'},
                'output_adapter': {'output_class': 'chatterbot.adapters.output.OutputFormatAdapter'},
                'database': self.create_test_data_directory()
        }

    def random_string(self, start=0, end=9000):
        """
        Generate a string based on a random number.
        """
        from random import randint
        return str(randint(start, end))

    def create_test_data_directory(self):
        self.test_data_directory = 'test_data'
        test_database_name = self.random_string() + '.db'

        if not os.path.exists(self.test_data_directory):
            os.makedirs(self.test_data_directory)

        return os.path.join(
            self.test_data_directory,
            test_database_name
        )

    def remove_test_data(self):
        import shutil

        if os.path.exists(self.test_data_directory):
            shutil.rmtree(self.test_data_directory)

    def tearDown(self):
        """
        Remove the test database.
        """
        self.chatbot.storage.drop()
        self.remove_test_data()


class ChatBotMongoTestCase(ChatBotTestCase):

    def setUp(self):
        from pymongo.errors import ServerSelectionTimeoutError
        from pymongo import MongoClient

        # Skip these tests if a mongo client is not running
        try:
            client = MongoClient(
                serverSelectionTimeoutMS=0.1
            )
            client.server_info()

            self.chatbot = ChatBot('Tester Bot', **self.get_kwargs())

        except ServerSelectionTimeoutError:
            raise SkipTest('Unable to connect to Mongo DB.')

    def get_kwargs(self):
        kwargs = super(ChatBotMongoTestCase, self).get_kwargs()
        kwargs['database'] = self.random_string()
        kwargs['storage_adapter'] = 'chatterbot.adapters.storage.MongoDatabaseAdapter'
        return kwargs

