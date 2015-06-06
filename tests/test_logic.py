from .base_case import ChatBotTestCase
from chatterbot.adapters.logic import ClosestMatchAdapter


class ClosestMatchAdapterTests(ChatBotTestCase):

    def test_get_closest_statement(self):

        adapter = ClosestMatchAdapter(self.chatbot.storage.storage_adapter)

        close = adapter.get("What is your quest?", )
        expected = "What... is your quest?"

        self.assertEqual(expected, close)
