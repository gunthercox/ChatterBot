from .base_case import ChatBotSQLTestCase
from chatterbot import response_selection
from chatterbot.conversation import Statement


class ResponseSelectionTests(ChatBotSQLTestCase):

    def test_get_most_frequent_response(self):
        statement_list = [
            Statement('What... is your quest?', in_response_to='Hello'),
            Statement('What... is your quest?', in_response_to='Hello'),
            Statement('This is a phone.', in_response_to='Hello'),
            Statement('This is a phone.', in_response_to='Hello'),
            Statement('This is a phone.', in_response_to='Hello'),
            Statement('This is a phone.', in_response_to='Hello'),
            Statement('A what?', in_response_to='Hello'),
            Statement('A what?', in_response_to='Hello'),
            Statement('A phone.', in_response_to='Hello')
        ]

        for statement in statement_list:
            self.chatbot.storage.create(
                text=statement.text,
                in_response_to=statement.in_response_to
            )

        output = response_selection.get_most_frequent_response(
            Statement('Hello'),
            statement_list,
            self.chatbot.storage
        )

        self.assertEqual('This is a phone.', output.text)

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
