from unittest import TestCase
from chatterbot.conversation import Statement
from chatterbot.conversation.session import Conversation, ConversationManager
from .base_case import ChatBotTestCase


class ConversationTestCase(TestCase):

    def setUp(self):
        super(ConversationTestCase, self).setUp()
        self.conversation = Conversation()

    def test_id(self):
        self.assertEqual(str(self.conversation.uuid), self.conversation.id)

    def test_no_last_response_statement(self):
        self.assertIsNone(self.conversation.get_last_response_statement())

    def test_get_last_response_statement(self):
        """
        Make sure that the get last statement method
        returns the last statement that was issued.
        """
        self.conversation.statements.add(Statement('Test statement 1'))
        self.conversation.statements.add(Statement('Test response 1'))
        self.conversation.statements.add(Statement('Test statement 2'))
        self.conversation.statements.add(Statement('Test response 2'))

        last_statement = self.conversation.get_last_response_statement()
        self.assertEqual(last_statement, 'Test response 2')

    def test_no_last_input_statement(self):
        self.assertIsNone(self.conversation.get_last_input_statement())

    def test_get_last_input_statement(self):
        """
        Make sure that the get last statement method
        returns the last statement that was issued.
        """
        self.conversation.statements.add(Statement('Test statement 1'))
        self.conversation.statements.add(Statement('Test response 1'))
        self.conversation.statements.add(Statement('Test statement 2'))
        self.conversation.statements.add(Statement('Test response 2'))

        last_statement = self.conversation.get_last_input_statement()
        self.assertEqual(last_statement, 'Test statement 2')


class ConversationManagerTestCase(ChatBotTestCase):

    def setUp(self):
        super(ConversationManagerTestCase, self).setUp()
        self.manager = ConversationManager(self.chatbot.storage)

    def test_new(self):
        conversation = self.manager.create()

        self.assertTrue(isinstance(conversation, Conversation))
        self.assertEqual(conversation.id, self.manager.get(conversation.id).id)

    def test_get(self):
        conversation = self.manager.create()
        returned_conversation = self.manager.get(conversation.id)

        self.assertEqual(conversation.id, returned_conversation.id)

    def test_get_invalid_id(self):
        returned_conversation = self.manager.get('--invalid--')

        self.assertIsNone(returned_conversation)

    def test_get_invalid_id_with_deafult(self):
        returned_conversation = self.manager.get('--invalid--', 'default_value')

        self.assertEqual(returned_conversation, 'default_value')

    def test_update(self):
        conversation = self.manager.create()
        self.manager.update(conversation.id, Statement('A'))

        conversation_ids =[]
        for conversation in self.manager.storage.filter(self.manager.storage.Conversation):
            conversation_ids.append(conversation.id)

        self.assertEqual(self.manager.get(conversation.id).statements.count(), 1)
        self.assertEqual(Statement('A'), self.manager.get(conversation.id).statements.first())

    def test_modify_chatbot(self):
        """
        When one adapter modifies its chatbot instance,
        the change should be the same in all other adapters.
        """
        conversation = self.chatbot.input.chatbot.conversation_sessions.create()
        self.chatbot.input.chatbot.conversation_sessions.update(
            conversation.id,
            Statement('A')
        )

        conversation = self.chatbot.output.chatbot.conversation_sessions.get(conversation.id)

        self.assertIn(Statement('A'), conversation.statements.all())

