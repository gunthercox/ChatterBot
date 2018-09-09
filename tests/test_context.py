from .base_case import ChatBotTestCase


class AdapterTests(ChatBotTestCase):

    def test_modify_chatbot(self):
        """
        When one adapter modifies its chatbot instance,
        the change should be the same in all other adapters.
        """
        self.chatbot.input.chatbot.read_only = 'TESTING'

        value = self.chatbot.output.chatbot.read_only

        self.assertEqual('TESTING', value)
