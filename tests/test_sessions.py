from unittest import TestCase
from chatterbot.conversation import Statement
from chatterbot.conversation.session import Session, ConversationSessionManager
from .base_case import ChatBotTestCase


class SessionTestCase(TestCase):

    def setUp(self):
        super(SessionTestCase, self).setUp()
        self.session = Session()

    def test_id(self):
        self.assertEqual(str(self.session.uuid), self.session.id)

    def test_no_last_response_statement(self):
        self.assertIsNone(self.session.get_last_response_statement())

    def test_get_last_response_statement(self):
        """
        Make sure that the get last statement method
        returns the last statement that was issued.
        """
        self.session.conversation.append(Statement('Test statement 1'))
        self.session.conversation.append(Statement('Test response 1'))
        self.session.conversation.append(Statement('Test statement 2'))
        self.session.conversation.append(Statement('Test response 2'))

        last_statement = self.session.get_last_response_statement()
        self.assertEqual(last_statement, 'Test response 2')

    def test_no_last_input_statement(self):
        self.assertIsNone(self.session.get_last_input_statement())

    def test_get_last_input_statement(self):
        """
        Make sure that the get last statement method
        returns the last statement that was issued.
        """
        self.session.conversation.append(Statement('Test statement 1'))
        self.session.conversation.append(Statement('Test response 1'))
        self.session.conversation.append(Statement('Test statement 2'))
        self.session.conversation.append(Statement('Test response 2'))

        last_statement = self.session.get_last_input_statement()
        self.assertEqual(last_statement, 'Test statement 2')


class ConversationSessionManagerTestCase(ChatBotTestCase):

    def setUp(self):
        super(ConversationSessionManagerTestCase, self).setUp()
        self.manager = ConversationSessionManager(self.chatbot.storage)

    def test_new(self):
        session = self.manager.new()

        self.assertTrue(isinstance(session, Session))
        self.assertEqual(session.id, self.manager.get(session.id).id)

    def test_get(self):
        session = self.manager.new()
        returned_session = self.manager.get(session.id)

        self.assertEqual(session.id, returned_session.id)

    def test_get_invalid_id(self):
        returned_session = self.manager.get('--invalid--')

        self.assertIsNone(returned_session)

    def test_get_invalid_id_with_deafult(self):
        returned_session = self.manager.get('--invalid--', 'default_value')

        self.assertEqual(returned_session, 'default_value')

    def test_update(self):
        session = self.manager.new()
        self.manager.update(session.id, Statement('A'))

        session_ids =[]
        for conversation in self.manager.storage.filter(self.manager.storage.Conversation):
            session_ids.append(conversation.id)

        self.assertEqual(len(self.manager.get(session.id).conversation), 1)
        self.assertEqual(Statement('A'), self.manager.get(session.id).conversation[0])

    def test_modify_chatbot(self):
        """
        When one adapter modifies its chatbot instance,
        the change should be the same in all other adapters.
        """
        session = self.chatbot.input.chatbot.conversation_sessions.new()
        self.chatbot.input.chatbot.conversation_sessions.update(
            session.id,
            Statement('A')
        )

        session = self.chatbot.output.chatbot.conversation_sessions.get(session.id)

        self.assertIn(Statement('A'), session.conversation)

