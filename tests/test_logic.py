from .base_case import ChatBotTestCase
from chatterbot.adapters.logic import ClosestMatchAdapter


class ClosestMatchAdapterTests(ChatBotTestCase):

    def test_get_closest_statement(self):

        adapter = ClosestMatchAdapter()

        possible_choices = [
            "Who do you love?",
            "What is the meaning of life?",
            "I am Iron Man.",
            "What... is your quest?",
            "Yuck, black licorice jelly beans.",
            "I hear you are going on a quest?",
        ]

        close = adapter.get("What is your quest?", possible_choices)

        self.assertEqual("What... is your quest?", close)
