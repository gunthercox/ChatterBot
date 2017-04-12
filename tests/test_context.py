from .base_case import ChatBotTestCase


class AdapterTests(ChatBotTestCase):

    def test_modify_chatbot(self):
        """
        When one adapter modifies its chatbot instance,
        the change should be the same in all other adapters.
        """
        session = self.chatbot.input.chatbot.conversation_sessions.new()
        self.chatbot.input.chatbot.conversation_sessions.update(
            session.id_string,
            ('A', 'B', )
        )

        session = self.chatbot.output.chatbot.conversation_sessions.get(
            session.id_string
        )

        self.assertIn(('A', 'B', ), session.conversation)
