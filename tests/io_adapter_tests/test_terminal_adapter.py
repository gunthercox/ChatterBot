from unittest import TestCase
from chatterbot.conversation import Statement
from chatterbot.adapters.io import TerminalAdapter


class TerminalAdapterTests(TestCase):
    """
    The terminal adapter is designed to allow
    interaction with the chat bot to occur through
    a command line interface.
    """

    def test_response_is_printed(self):
        """
        This test ensures that the bot's response is
        correctly printed in the terminal.
        """
        # TODO: How can you test this?
        self.assertTrue(True)

    def test_response_is_returned(self):
        """
        For consistency across io adapters, the
        terminal adaper should return the output value. 
        """
        adapter = TerminalAdapter()
        statement = Statement("Come with me if you want to live.")

        self.assertEqual(
            adapter.process_response(statement),
            statement.text
        )

