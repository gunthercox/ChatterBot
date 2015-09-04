from unittest import TestCase
from chatterbot.adapters.logic import ClosestMatchAdapter


class ClosestMatchAdapterTests(TestCase):

    def setUp(self):
        self.adapter = ClosestMatchAdapter()

    def test_get_closest_statement(self):
        possible_choices = [
            "Who do you love?",
            "What is the meaning of life?",
            "I am Iron Man.",
            "What... is your quest?",
            "Yuck, black licorice jelly beans.",
            "I hear you are going on a quest?",
        ]

        close = self.adapter.get("What is your quest?", possible_choices)

        self.assertEqual("What... is your quest?", close)

    def test_no_choices(self):
        possible_choices = []
        close = self.adapter.get("What is your quest?", possible_choices)

        self.assertEqual("What is your quest?", close)

