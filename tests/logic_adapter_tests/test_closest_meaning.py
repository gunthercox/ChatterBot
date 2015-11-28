from unittest import TestCase
from chatterbot.adapters.logic import ClosestMeaningAdapter
from chatterbot.conversation import Statement


class ClosestMeaningAdapterTests(TestCase):

    def setUp(self):
        self.adapter = ClosestMeaningAdapter()

    def test_no_choices(self):
        possible_choices = []
        statement = Statement("Hello")

        close = self.adapter.get(statement, possible_choices)

        self.assertEqual("Hello", close)

    def test_get_closest_statement(self):
        possible_choices = [
            Statement("This is a lovely bog."),
            Statement("This is a beautiful swamp."),
            Statement("It smells like swamp.")
        ]
        statement = Statement("This is a lovely swamp.")

        close = self.adapter.get(statement, possible_choices)

        self.assertEqual("This is a lovely bog.", close)
