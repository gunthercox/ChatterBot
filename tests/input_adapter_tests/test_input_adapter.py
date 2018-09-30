from tests.base_case import ChatBotTestCase
from chatterbot.conversation import Statement
from chatterbot.input import InputAdapter


class InputAdapterTestCase(ChatBotTestCase):
    """
    Test case for the InputAdapter class.
    """

    def setUp(self):
        super().setUp()
        self.adapter = InputAdapter(self.chatbot)

    def test_process_input_statement(self):
        statement = self.adapter.process_input(Statement(text='Test'))

        self.assertEqual(statement.text, 'Test')

    def test_process_input_dict(self):
        data = {
            'text': 'Robot ipsum datus scan amet.'
        }
        statement = self.adapter.process_input(data)

        self.assertEqual(statement.text, data['text'])

    def test_process_input_text(self):
        text = 'The test statement to process is here.'
        statement = self.adapter.process_input(text)

        self.assertEqual(statement.text, text)

    def test_process_invalid_input_type(self):
        data = ['A list', 'of text', 'is an', 'invalid input type.']

        with self.assertRaises(InputAdapter.UnrecognizedInputFormatException):
            self.adapter.process_input(data)
