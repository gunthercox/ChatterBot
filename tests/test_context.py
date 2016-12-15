from .base_case import ChatBotTestCase


class AdapterTests(ChatBotTestCase):

    def setUp(self):
        super(AdapterTests, self).setUp()

    def test_modify_chatbot(self):
        """
        When one adapter modifies its chatbot instance,
        the change should be the same in all other adapters.
        """
        self.chatbot.input.chatbot.conversation_sessions.update_default(
            ('A', 'B', )
        )
        session = self.chatbot.output.chatbot.conversation_sessions.get_default()

        self.assertIn(('A', 'B', ), session.conversation)
