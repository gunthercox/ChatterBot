from unittest import TestCase
from chatterbot.adapters.logic import ClosestMatchAdapter
from chatterbot.conversation import Statement


class ClosestMatchAdapterTests(TestCase):

    def setUp(self):
        self.adapter = ClosestMatchAdapter()

    def test_get_closest_statement(self):
        possible_choices = [
            Statement("Who do you love?"),
            Statement("What is the meaning of life?"),
            Statement("I am Iron Man."),
            Statement("What... is your quest?"),
            Statement("Yuck, black licorice jelly beans."),
            Statement("I hear you are going on a quest?"),
        ]
        statement = Statement("What is your quest?")

        close = self.adapter.get(statement, possible_choices)

        self.assertEqual("What... is your quest?", close)

    def test_no_choices(self):
        possible_choices = []
        statement = Statement("What is your quest?")

        close = self.adapter.get(statement, possible_choices)

        self.assertEqual("What is your quest?", close)

