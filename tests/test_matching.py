from .base_case import ChatBotTestCase
from chatterbot.algorithms.matching import closest


class MatchingTests(ChatBotTestCase):

    def test_get_closest_statement(self):

        close = closest("What is your quest?", self.chatbot.database.path)
        expected = "What... is your quest?"

        self.assertEqual(expected, close)
