from unittest import TestCase
from chatterbot.conversation import Statement
from chatterbot.input import VariableInputTypeAdapter


class VariableInputTypeAdapterTests(TestCase):

    def setUp(self):
        self.adapter = VariableInputTypeAdapter()

    def test_statement_returned_dict(self):
        data = {
            'text': 'Robot ipsum datus scan amet.',
            'in_response_to': []
        }
        response = self.adapter.process_input(data)

        self.assertEqual(response.text, data['text'])

    def test_statement_returned_text(self):
        text = 'The test statement to process is here.'
        response = self.adapter.process_input(text)

        self.assertEqual(response.text, text)

    def test_statement_returned_object(self):
        statement = Statement('The test statement to process is here.')
        response = self.adapter.process_input(statement)

        self.assertEqual(response.text, statement.text)

    def test_invalid_input_type(self):
        data = ['A list', 'of text', 'is an', 'invalid input type.']

        with self.assertRaises(VariableInputTypeAdapter.UnrecognizedInputFormatException):
            self.adapter.process_input(data)
