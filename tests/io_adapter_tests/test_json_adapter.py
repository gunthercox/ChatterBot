from unittest import TestCase
from chatterbot.conversation import Statement
from chatterbot.adapters.io import JsonAdapter


class JsonAdapterTests(TestCase):

    def setUp(self):
        self.adapter = JsonAdapter()

    def test_response_json_returned(self):
        statement = Statement("Robot ipsum datus scan amet.")
        response = self.adapter.process_response(statement)

        self.assertEqual(statement.text, response["text"])
        self.assertIn("in_response_to", response)

