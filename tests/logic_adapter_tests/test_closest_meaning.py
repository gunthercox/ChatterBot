from unittest import TestCase
from chatterbot.adapters.logic import ClosestMeaningAdapter
from chatterbot.conversation import Statement


class ClosestMeaningAdapterTests(TestCase):

    def setUp(self):
        self.adapter = ClosestMeaningAdapter()

    def test_no_choices(self):
        possible_choices = []
        close = self.adapter.get("Hello", possible_choices)

        self.assertEqual("Hello", close)

    def test_get_closest_statement(self):
        possible_choices = [
            Statement("This is a lovely bog."),
            Statement("This is a beautiful swamp."),
            Statement("It smells like swamp.")
        ]

        close = self.adapter.get("This is a lovely swamp.", possible_choices)

        self.assertEqual("This is a lovely bog.", close)

