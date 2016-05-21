from .base_case import ChatBotTestCase


class ContextTests(ChatBotTestCase):

    def setUp(self):
        super(ContextTests, self).setUp()

    def test_modify_context(self):
        """
        When one adapter changes the context,
        the change should be the same in all
        other adapters.
        """
        self.chatbot.input.context.recent_statements = [5]
        data = self.chatbot.output.context.recent_statements

        self.assertIn(5, data)
