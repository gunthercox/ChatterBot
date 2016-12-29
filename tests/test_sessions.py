from unittest import TestCase
from chatterbot.conversation.session import Session, ConversationSessionManager


class SessionTestCase(TestCase):

    def test_id_string(self):
        session = Session()
        self.assertEqual(str(session.uuid), session.id_string)


class ConversationSessionManagerTestCase(TestCase):

    def setUp(self):
        super(ConversationSessionManagerTestCase, self).setUp()
        self.manager = ConversationSessionManager()

    def test_new(self):
        session = self.manager.new()

        self.assertTrue(isinstance(session, Session))
        self.assertIn(session.id_string, self.manager.sessions)
        self.assertEqual(session, self.manager.sessions[session.id_string])

    def test_get(self):
        session = self.manager.new()
        returned_session = self.manager.get(session.id_string)

        self.assertEqual(session.id_string, returned_session.id_string)

    def test_get_invalid_id(self):
        returned_session = self.manager.get('--invalid--')

        self.assertIsNone(returned_session)

    def test_get_invalid_id_with_deafult(self):
        returned_session = self.manager.get('--invalid--', 'default_value')

        self.assertEqual(returned_session, 'default_value')

    def test_update(self):
        session = self.manager.new()
        self.manager.update(session.id_string, ('A', 'B', ))

        session_ids = list(self.manager.sessions.keys())
        session_id = session_ids[0]

        self.assertEqual(len(session_ids), 1)
        self.assertEqual(len(self.manager.get(session_id).conversation), 1)
        self.assertEqual(('A', 'B', ), self.manager.get(session_id).conversation[0])
