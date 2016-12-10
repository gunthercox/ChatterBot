from django.test import TestCase
from django.core.exceptions import ValidationError
from chatterbot.ext.django_chatterbot.views import ChatterBotView


class MockResponse(object):

    def __init__(self, id_string):
        self.session = {'chat_session_id': id_string}


class ViewTestCase(TestCase):

    def setUp(self):
        super(ViewTestCase, self).setUp()
        self.view = ChatterBotView()

    def test_validate_text(self):
        try:
            self.view.validate({
                'text': 'How are you?'
            })
        except ValidationError:
            self.fail('Test raised ValidationError unexpectedly!')

    def test_validate_invalid_text(self):
        with self.assertRaises(ValidationError):
            self.view.validate({
                'type': 'classmethod'
            })

    def test_get_chat_session(self):
        session = self.view.chatterbot.conversation_sessions.new()
        mock_response = MockResponse(session.id_string)
        get_session = self.view.get_chat_session(mock_response)

        self.assertEqual(session.id_string, get_session.id_string)

    def test_get_chat_session_invalid(self):
        mock_response = MockResponse('--invalid--')
        session = self.view.get_chat_session(mock_response)

        self.assertNotEqual(session.id_string, 'test-session-id')

    def test_get_chat_session_no_session(self):
        mock_response = MockResponse(None)
        mock_response.session = {}
        session = self.view.get_chat_session(mock_response)

        self.assertNotEqual(session.id_string, 'test-session-id')
