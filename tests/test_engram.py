from .base_case import ChatBotTestCase
from chatterbot.algorithms.engram import engram


class EngramTests(ChatBotTestCase):

    def test_exact_results(self):

        output = engram("What... is your quest?", self.chatbot.database.path)
        expected = "To seek the Holy Grail."

        self.assertEqual(len(output), 1)
        self.assertIn(expected, output.keys())

    def test_close_results(self):

        output = engram("What is your quest?", self.chatbot.database.path)
        expected = "To seek the Holy Grail."

        self.assertEqual(len(output), 1)
        self.assertIn(expected, output.keys())

    def test_empty_input(self):

        output = engram("", self.chatbot.database.path)

        self.assertEqual(len(output), 1)

    def test_get_closest_statement(self):
        from chatterbot.algorithms.engram import get_closest_statement

        closest = get_closest_statement("What is your quest?", self.chatbot.database.path)
        expected = "What... is your quest?"

        self.assertIn(expected, closest.keys())
