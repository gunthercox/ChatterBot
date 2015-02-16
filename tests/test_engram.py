from .base_case import ChatBotTestCase
from chatterbot.algorithms.engram import engram


class EngramTests(ChatBotTestCase):

    def test_exact_results(self):

        output = engram("What... is your quest?", self.chatbot.database)
        expected = "To seek the Holy Grail."

        self.assertEqual(len(output), 1)
        self.assertIn(expected, output.keys())

    def test_close_results(self):

        output = engram("What is your quest?", self.chatbot.database)
        expected = "To seek the Holy Grail."

        self.assertEqual(len(output), 1)
        self.assertIn(expected, output.keys())

    def test_empty_input(self):

        output = engram("", self.chatbot.database)

        self.assertEqual(len(output), 1)
