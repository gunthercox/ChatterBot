from django.test import TestCase
from django.core.exceptions import ValidationError
from chatterbot.ext.django_chatterbot.views import ChatterBotView


class MockResponse(object):

    def __init__(self, pk):
        self.session = {'chat_session_id': pk}


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

    def test_get_conversation(self):
        from chatterbot.ext.django_chatterbot.models import Statement, Phrase

        conversation_id = self.view.chatterbot.storage.create_conversation()

        statement = Statement.objects.create(
            text='Test statement',
            phrase=Phrase.objects.create(
                text='Test statement'
            )
        )
        statement.phrase.conversations.add(conversation_id)

        mock_response = MockResponse(conversation_id)
        get_session = self.view.get_conversation(mock_response)

        self.assertEqual(conversation_id, get_session.id)

    def test_get_conversation_invalid(self):
        mock_response = MockResponse(0)
        session = self.view.get_conversation(mock_response)

        self.assertNotEqual(session.id, 'test-session-id')

    def test_get_conversation_no_session(self):
        mock_response = MockResponse(None)
        mock_response.session = {}
        session = self.view.get_conversation(mock_response)

        self.assertNotEqual(session.id, 'test-session-id')
