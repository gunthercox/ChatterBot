"""
Tests for using DjangoStorageAdapter with a secondary database.
"""
from tests.django_integration.base_case import ChatterBotTestCase
from chatterbot import ChatBot


class SecondaryDatabaseTestCase(ChatterBotTestCase):
    """
    Test that the database parameter can be passed to DjangoStorageAdapter.
    """

    def setUp(self):
        super().setUp()

        # Create a chatbot that explicitly uses the 'default' database
        self.chatbot = ChatBot(
            'Test Bot',
            storage_adapter='chatterbot.storage.DjangoStorageAdapter',
            database='default',
            logic_adapters=[
                'chatterbot.logic.BestMatch'
            ]
        )

    def test_database_parameter_accepted(self):
        """
        Test that the database parameter is accepted and stored.
        """
        self.assertEqual(self.chatbot.storage.database, 'default')

    def test_database_parameter_default(self):
        """
        Test that the database parameter defaults to 'default' if not specified.
        """
        chatbot = ChatBot(
            'Test Bot 2',
            storage_adapter='chatterbot.storage.DjangoStorageAdapter'
        )
        self.assertEqual(chatbot.storage.database, 'default')

    def test_operations_with_database_parameter(self):
        """
        Test that basic operations work with the database parameter set.
        """
        # Create a statement
        statement = self.chatbot.storage.create(
            text='Hello',
            conversation='test'
        )

        self.assertIsNotNone(statement)
        self.assertEqual(statement.text, 'Hello')

        # Count statements
        count = self.chatbot.storage.count()
        self.assertGreater(count, 0)

        # Filter statements
        results = list(self.chatbot.storage.filter(text='Hello'))
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].text, 'Hello')

        # Remove statement
        self.chatbot.storage.remove('Hello')

        # Verify removal
        count_after = self.chatbot.storage.count()
        self.assertEqual(count_after, count - 1)
