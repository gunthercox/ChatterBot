from .base_case import ChatBotTestCase


class AdapterTests(ChatBotTestCase):

    def setUp(self):
        super(AdapterTests, self).setUp()

    def test_modify_chatbot(self):
        """
        When one adapter modifies its chatbot instance,
        the change should be the same in all other adapters.
        """
        self.chatbot.input.chatbot.recent_statements = [5]
        data = self.chatbot.output.chatbot.recent_statements

        self.assertIn(5, data)
