from unittest import TestCase
from chatterbot.adapters.logic import ClosestMeaningAdapter
from chatterbot.conversation import Statement


class ClosestMeaningAdapterTests(TestCase):

    def setUp(self):
        self.adapter = ClosestMeaningAdapter()

    def test_no_choices(self):
        from chatterbot.adapters.exceptions import EmptyDatasetException

        possible_choices = []
        statement = Statement("Hello")

        with self.assertRaises(EmptyDatasetException):
            self.adapter.get(statement, possible_choices)

    def test_get_closest_statement(self):
        possible_choices = [
            Statement("This is a lovely bog."),
            Statement("This is a beautiful swamp."),
            Statement("It smells like swamp.")
        ]
        statement = Statement("This is a lovely swamp.")

        confidence, match = self.adapter.get(statement, possible_choices)

        self.assertEqual("This is a lovely bog.", match)

