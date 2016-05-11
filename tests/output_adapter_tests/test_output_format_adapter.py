from unittest import TestCase
from chatterbot.conversation import Statement
from chatterbot.adapters.output import OutputFormatAdapter


class OutputFormatAdapterTests(TestCase):

    def test_response_json_returned(self):
        adapter = OutputFormatAdapter(output_format='json')

        statement = Statement('Robot ipsum datus scan amet.')
        response = adapter.process_response(statement)

        self.assertIn('text', response)
        self.assertEqual(statement.text, response['text'])
        self.assertIn('in_response_to', response)

    def test_response_text_is_returned(self):
        adapter = OutputFormatAdapter(output_format='text')

        statement = Statement('The test statement to process is here.')
        response = adapter.process_response(statement)

        self.assertEqual(response, statement.text)

    def test_response_object_is_returned(self):
        adapter = OutputFormatAdapter(output_format='object')

        statement = Statement('The test statement to process is here.')
        response = adapter.process_response(statement)

        self.assertEqual(response, statement)

    def test_response_object_is_returned_if_not_specified(self):
        adapter = OutputFormatAdapter()

        statement = Statement('The test statement to process is here.')
        response = adapter.process_response(statement)

        self.assertEqual(response, statement)

    def test_invalid_output_format(self):
        with self.assertRaises(OutputFormatAdapter.UnrecognizedOutputFormatException):
            OutputFormatAdapter(output_format='invalid')
