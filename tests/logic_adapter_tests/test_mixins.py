from unittest import TestCase
from chatterbot.adapters.logic.mixins import TieBreaking
from chatterbot.conversation import Statement, Response


class TieBreakingTests(TestCase):

    def setUp(self):
        self.mixin = TieBreaking()

    def test_get_most_frequent_response(self):
        statement_list = [
            Statement('What... is your quest?', in_response_to=[Response('Hello', occurrence=2)]),
            Statement('This is a phone.', in_response_to=[Response('Hello', occurrence=4)]),
            Statement('A what?', in_response_to=[Response('Hello', occurrence=2)]),
            Statement('A phone.', in_response_to=[Response('Hello', occurrence=1)])
        ]

        output = self.mixin.get_most_frequent_response(
            Statement('Hello'),
            statement_list
        )

        self.assertEqual('This is a phone.', output)

    def test_get_first_response(self):
        statement_list = [
            Statement('What... is your quest?'),
            Statement('A what?'),
            Statement('A quest.')
        ]

        output = self.mixin.get_first_response(Statement('Hello'), statement_list)

        self.assertEqual('What... is your quest?', output)

    def test_get_random_response(self):
        statement_list = [
            Statement('This is a phone.'),
            Statement('A what?'),
            Statement('A phone.')
        ]

        output = self.mixin.get_random_response(Statement('Hello'), statement_list)

        self.assertTrue(output)

    def test_break_tie_get_first_response(self):
        statement_list = [
            Statement('What... is your quest?'),
            Statement('A what?'),
            Statement('A quest.')
        ]

        output = self.mixin.break_tie(Statement('Hello'), statement_list, 'first_response')

        self.assertEqual('What... is your quest?', output)

    def test_break_tie_invalid_method(self):
        with self.assertRaises(TieBreaking.InvalidTieBreakingMethodException):
            self.mixin.break_tie(Statement('Hello'), [], 'invalid_method')
