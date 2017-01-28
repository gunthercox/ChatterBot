from django.test import TestCase
from django.core.exceptions import ValidationError
from chatterbot.ext.django_chatterbot.views import ChatterBotView


class MockResponse(object):

    def __init__(self, pk):
        self.session = {'chat_conversation_id': pk}


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
        conversation = self.view.chatterbot.conversations.create()
        mock_response = MockResponse(conversation.id)
        get_conversation = self.view.get_conversation(mock_response)

        self.assertEqual(conversation.id, get_conversation.id)

    def test_get_conversation_invalid(self):
        mock_response = MockResponse(0)
        conversation = self.view.get_conversation(mock_response)

        self.assertNotEqual(conversation.id, 0)

    def test_get_conversation_no_conversation(self):
        mock_response = MockResponse(None)
        mock_response.session = {}
        conversation = self.view.get_conversation(mock_response)

        self.assertNotEqual(conversation.id, None)
