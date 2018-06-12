from django.test import TestCase
from example_app.views import ChatterBotApiView


class MockResponse(object):

    def __init__(self, pk):
        self.session = {'conversation_id': pk}


class ViewTestCase(TestCase):

    def setUp(self):
        super(ViewTestCase, self).setUp()
        self.view = ChatterBotApiView()

    def test_get_conversation(self):
        conversation_id = self.view.chatterbot.storage.create_conversation()

        mock_response = MockResponse(conversation_id)
        conversation = self.view.get_conversation(mock_response)

        self.assertEqual(conversation_id, conversation.id)

    def test_get_conversation_invalid(self):
        mock_response = MockResponse(0)
        session = self.view.get_conversation(mock_response)

        self.assertNotEqual(session.id, 'test-session-id')

    def test_get_conversation_nonexistent(self):
        mock_response = MockResponse(None)
        mock_response.session = {}
        session = self.view.get_conversation(mock_response)

        self.assertNotEqual(session.id, 'test-session-id')
