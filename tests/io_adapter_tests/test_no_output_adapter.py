from unittest import TestCase
from chatterbot.conversation import Statement
from chatterbot.adapters.io import NoOutputAdapter


class NoOutputAdapterTests(TestCase):
    """
    The no output adapter is designed to allow
    the chat bot to be used like a library, without
    assuming any single form of communication
    is used.
    """

    def setUp(self):
        self.adapter = NoOutputAdapter()

    def test_response_is_returned(self):
        """
        For consistency across io adapters, the
        no output adaper should return the output value.
        """
        statement = Statement("The test statement to process is here.")

        self.assertEqual(
            self.adapter.process_response(statement),
            statement.text
        )

