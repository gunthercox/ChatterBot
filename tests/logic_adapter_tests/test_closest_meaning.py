from unittest import TestCase
from chatterbot.adapters.logic import ClosestMeaningAdapter
from chatterbot.conversation import Statement, Response


class ClosestMeaningAdapterTests(TestCase):

    def setUp(self):
        self.adapter = ClosestMeaningAdapter()

    def test_no_choices(self):
        possible_choices = []
        statement = Statement("Hello")

        with self.assertRaises(ClosestMeaningAdapter.EmptyDatasetException):
            self.adapter.get(statement, possible_choices)

    def test_get_closest_statement(self):
        """
        Note, the content of the in_response_to field for each of the
        test statements is only required because the logic adapter will
        filter out any statements that are not in response to a known statement.
        """
        possible_choices = [
            Statement("This is a lovely bog.", in_response_to=[Response("This is a lovely bog.")]),
            Statement("This is a beautiful swamp.", in_response_to=[Response("This is a beautiful swamp.")]),
            Statement("It smells like swamp.", in_response_to=[Response("It smells like swamp.")])
        ]
        statement = Statement("This is a lovely swamp.")

        confidence, match = self.adapter.get(statement, possible_choices)

        self.assertEqual("This is a lovely bog.", match)

