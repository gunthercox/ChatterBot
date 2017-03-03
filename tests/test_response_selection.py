from unittest import TestCase
from chatterbot import response_selection
from chatterbot.conversation import Statement, Response


class ResponseSelectionTests(TestCase):

    def test_get_most_frequent_response(self):
        statement_list = [
            Statement('What... is your quest?', in_response_to=[Response('Hello', occurrence=2)]),
            Statement('This is a phone.', in_response_to=[Response('Hello', occurrence=4)]),
            Statement('A what?', in_response_to=[Response('Hello', occurrence=2)]),
            Statement('A phone.', in_response_to=[Response('Hello', occurrence=1)])
        ]

        output = response_selection.get_most_frequent_response(
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

        output = response_selection.get_first_response(Statement('Hello'), statement_list)

        self.assertEqual('What... is your quest?', output)

    def test_get_random_response(self):
        statement_list = [
            Statement('This is a phone.'),
            Statement('A what?'),
            Statement('A phone.')
        ]

        output = response_selection.get_random_response(Statement('Hello'), statement_list)

        self.assertTrue(output)
