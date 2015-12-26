from unittest import TestCase
from chatterbot.adapters.logic import LogicAdapter
from chatterbot.adapters.logic.mixins import KnownResponseMixin, ResponseSelectionMixin
from chatterbot import ChatBot
from chatterbot.conversation import Statement
import os


class DummyMutatorLogicAdapter(KnownResponseMixin, ResponseSelectionMixin, LogicAdapter):
    """
    This is a dummy class designed to modify a
    the resulting statement before it is returned.
    """

    def get(self, text, statement_list=None):
        statement = Statement("Hello")
        statement.add_extra_data("pos_tags", "NN")

        return statement


class DataCachingTests(TestCase):

    def setUp(self):
        self.test_data_directory = 'test_data'
        self.test_database_name = self.random_string() + ".db"

        if not os.path.exists(self.test_data_directory):
            os.makedirs(self.test_data_directory)

        database_path = os.path.join(
            self.test_data_directory,
            self.test_database_name
        )

        self.chatbot = ChatBot(
            "Test Bot",
            io_adapter="chatterbot.adapters.io.NoOutputAdapter",
            logic_adapter="tests.logic_adapter_tests.test_data_cache.DummyMutatorLogicAdapter",
            database=database_path
        )

        self.chatbot.train([
            "Hello",
            "How are you?"
        ])

    def random_string(self, start=0, end=9000):
        """
        Generate a string based on a random number.
        """
        from random import randint
        return str(randint(start, end))

    def remove_data(self):
        import shutil

        if os.path.exists(self.test_data_directory):
            shutil.rmtree(self.test_data_directory)

    def tearDown(self):
        """
        Remove the test database.
        """
        self.chatbot.storage.drop()
        self.remove_data()

    def test_modified_statement_saved(self):
        statement = Statement("How are you?")
        response = self.chatbot.get_response("Hello")
        found_statement = self.chatbot.storage.find(statement.text)

        # The dummy adapter should always return the same response statement
        self.assertEqual(response, statement)
        self.assertIsNotNone(found_statement)

    def test_additional_attributes_saved(self):
        """
        Test that an additional data attribute can be added to the statement
        and that this attribute is saved.
        """
        response = self.chatbot.get_response("Hello")
        found_statement = self.chatbot.storage.find("Hello")

        self.assertIsNotNone(found_statement)
        self.assertIn("pos_tags", found_statement.serialize())
        self.assertEqual(
            "NN",
            found_statement.serialize()["pos_tags"]
        )

