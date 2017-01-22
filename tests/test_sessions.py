from unittest import TestCase
from chatterbot.conversation.session import Session, ConversationSessionManager
from .base_case import ChatBotTestCase


class SessionTestCase(TestCase):

    def test_id(self):
        session = Session()
        self.assertEqual(str(session.uuid), session.id)


class ConversationSessionManagerTestCase(ChatBotTestCase):

    def setUp(self):
        super(ConversationSessionManagerTestCase, self).setUp()
        self.manager = ConversationSessionManager(self.chatbot.storage)

    def test_new(self):
        session = self.manager.new()

        self.assertTrue(isinstance(session, Session))
        self.assertIn(session.id, self.manager.sessions)
        self.assertEqual(session, self.manager.sessions[session.id])

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
        self.manager.update(session.id, ('A', 'B', ))

        session_ids = list(self.manager.sessions.keys())
        session_id = session_ids[0]

        self.assertEqual(len(session_ids), 1)
        self.assertEqual(len(self.manager.get(session_id).conversation), 1)
        self.assertEqual(('A', 'B', ), self.manager.get(session_id).conversation[0])
