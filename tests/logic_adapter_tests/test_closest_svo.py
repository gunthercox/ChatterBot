from unittest import TestCase
from chatterbot.adapters.logic import ClosestSVOAdapter


class ClosestSVOAdapterTests(TestCase):

    def setUp(self):
        self.adapter = ClosestSVOAdapter()

    def test_get_closest_statement(self):
        possible_choices = [
            "This is a lovely bog.",
            "This is a beautiful swamp.",
            "It smells like swamp."
        ]

        close = self.adapter.get("This is a lovely swamp.", possible_choices)

        self.assertEqual("This is a beautiful swamp.", close)

    def test_no_choices(self):
        possible_choices = []
        close = self.adapter.get("What is your quest?", possible_choices)

        self.assertEqual("What is your quest?", close)
