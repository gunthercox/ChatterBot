from unittest import TestCase
from chatterbot.adapters.io import TerminalAdapter


class TerminalAdapterTests(TestCase):
    """
    The terminal adapter is designed to allow
    interaction with the chat bot to occur through
    a command line interface.a command line interface.
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

        test_data = {
            "user": {
                "Come with me if you want to live.": {}
            },
            "bot": {
                "Fortunately for you, my process cannot be terminated.": {}
            }
        }

        adapter = TerminalAdapter()

        response = adapter.process_response(test_data)

        self.assertEqual(
            "Fortunately for you, my process cannot be terminated.",
            response
        )
