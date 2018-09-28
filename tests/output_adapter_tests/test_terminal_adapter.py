from tests.base_case import ChatBotTestCase
from chatterbot.conversation import Statement
from chatterbot.output import TerminalAdapter


class TerminalAdapterTests(ChatBotTestCase):
    """
    The terminal adapter is designed to allow
    interaction with the chat bot to occur through
    a command line interface.
    """

    def setUp(self):
        super().setUp()
        self.adapter = TerminalAdapter(self.chatbot)

    def test_response_is_returned(self):
        """
        For consistency across io adapters, the
        terminal adaper should return the output value.
        """
        statement = Statement("Come with me if you want to live.")

        self.assertEqual(
            self.adapter.process_response(statement),
            statement.text
        )
