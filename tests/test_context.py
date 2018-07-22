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

    def test_get_latest_response(self):
        from chatterbot.conversation import Statement, Response
        conversation = 'test'

        self.chatbot.storage.update(Statement(text='A'))
        self.chatbot.storage.update(Statement(text='B', in_response_to=[
            Response(text='A', conversation=conversation)
        ]))

        response_statement = self.chatbot.storage.get_latest_response(
            conversation
        )

        self.assertEqual('A', response_statement.text)
