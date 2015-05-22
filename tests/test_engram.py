from .base_case import ChatBotTestCase
from chatterbot.adapters.logic.engram import EngramAdapter
from chatterbot.adapters.logic.matching import closest


class EngramTests(ChatBotTestCase):

    def test_exact_results(self):

        output = EngramAdapter(self.chatbot.storage)
        expected = "To seek the Holy Grail."

        self.assertIn(expected, output.get("What... is your quest?").keys())

    def test_empty_input(self):
        """
        If empty input is provided, anything may be returned.
        """
        output = self.chatbot.get_response("")

        self.assertTrue(len(output) > -1)


class MatchingTests(ChatBotTestCase):

    def test_get_closest_statement(self):

        close = closest("What is your quest?", self.chatbot.storage)
        expected = "What... is your quest?"

        self.assertEqual(expected, close)
