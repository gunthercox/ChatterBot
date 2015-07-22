from unittest import TestCase
from chatterbot import ChatBot


class ChatBotTestCase(TestCase):

    def setUp(self):
        """
        Set up a database for testing.
        """
        data1 = [
            "african or european?",
            "Huh? I... I don't know that.",
            "How do you know so much about swallows?"
        ]

        data2 = [
            "Siri is adorable",
            "Who is Seri?",
            "Siri is my cat"
        ]

        data3 = [
            "What... is your quest?",
            "To seek the Holy Grail.",
            "What... is your favourite colour?",
            "Blue."
        ]

        self.chatbot = ChatBot("Test Bot", database="test-database.db")

        self.chatbot.train(data1)
        self.chatbot.train(data2)
        self.chatbot.train(data3)

    def tearDown(self):
        """
        Remove the test database.
        """
        self.chatbot.storage.storage_adapter.drop()


class UntrainedChatBotTestCase(TestCase):
    """
    This is a test case for use when the
    chat bot should not start with any
    prior training.
    """

    def setUp(self):
        """
        Set up a database for testing.
        """
        test_db = self.random_string() + ".db"
        self.chatbot = ChatBot("Test Bot", database=test_db)

    def random_string(self, start=0, end=9000):
        """
        Generate a string based on a random number.
        """
        from random import randint
        return str(randint(start, end))

    def tearDown(self):
        """
        Remove the test database.
        """
        self.chatbot.storage.storage_adapter.drop()

