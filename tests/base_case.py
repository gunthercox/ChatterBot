from unittest import TestCase
from chatterbot import ChatBot


class ChatBotTestCase(TestCase):

    def setUp(self):
        """
        Set up a database for testing.
        """
        import os

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

        self.chatbot = ChatBot("Test Bot")
        self.chatbot.database.set_path("test-database.db")

        self.chatbot.train(data1)
        self.chatbot.train(data2)
        self.chatbot.train(data3)

    def tearDown(self):
        """
        Remove the log files that were created for testing.
        """
        import os

        os.remove(self.chatbot.database.path)
