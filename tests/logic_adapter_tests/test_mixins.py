from unittest import TestCase
from ..base_case import ChatBotTestCase
from chatterbot.adapters.logic.mixins import TieBreaking
from chatterbot.conversation import Statement, Response


class TieBreakingTests(TestCase):

    def setUp(self):
        self.mixin = TieBreaking()

    def test_get_most_frequent_response(self):
        statement_list = [
            Statement("What... is your quest?", in_response_to=[Response("Hello", occurrence=2)]),
            Statement("This is a phone.", in_response_to=[Response("Hello", occurrence=4)]),
            Statement("A what?", in_response_to=[Response("Hello", occurrence=2)]),
            Statement("A phone.", in_response_to=[Response("Hello", occurrence=1)])
        ]

        output = self.mixin.get_most_frequent_response(
            Statement("Hello"),
            statement_list
        )

        self.assertEqual("This is a phone.", output)

    def test_get_first_response(self):
        statement_list = [
            Statement("What... is your quest?"),
            Statement("A what?"),
            Statement("A quest.")
        ]

        output = self.mixin.get_first_response(statement_list)

        self.assertEqual("What... is your quest?", output)

    def test_get_random_response(self):
        statement_list = [
            Statement("This is a phone."),
            Statement("A what?"),
            Statement("A phone.")
        ]

        output = self.mixin.get_random_response(statement_list)

        self.assertTrue(output)

