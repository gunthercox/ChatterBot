from unittest import TestCase
from chatterbot.conversation import Statement
from chatterbot.adapters.io import MacOSXTTS


class MacOSXTTSTests(TestCase):
    """
    The MacOSXTTS adapter is designed to allow
    interaction with the chat bot to occur through
    a command line interface and via speech.
    """

    def setUp(self):
        self.adapter = MacOSXTTS()

    def test_response_is_returned(self):
        """
        For consistency across io adapters, the
        MacOSXTTS should return the output value.
        """
        statement = Statement("Testing speech synthesis.")

        self.assertEqual(
            self.adapter.process_response(statement),
            statement.text
        )
