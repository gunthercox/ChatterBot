from .base_case import ChatBotTestCase


class ChatBotTests(ChatBotTestCase):

    def test_get_last_statement(self):
        """
        Make sure that the get last statement method
        returns the last statement that was issued.
        """
        self.chatbot.last_statements.append("Test statement")

        self.assertEqual(self.chatbot.get_last_statement(), "Test statement")
