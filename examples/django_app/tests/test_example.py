import json
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.utils.encoding import force_text
from chatterbot.ext.django_chatterbot.views import ChatterBotView


class ViewTestCase(TestCase):

    def setUp(self):
        super(ViewTestCase, self).setUp()
        self.url = reverse('main')

    def test_get_main_page(self):
        """
        Test that the main page can be loaded.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)


class ApiTestCase(TestCase):
    """
    Tests to make sure that the ChatterBot app is
    properly working with the Django example app.
    """

    def setUp(self):
        super(ApiTestCase, self).setUp()
        self.api_url = reverse('chatterbot:chatterbot')

    def test_post(self):
        """
        Test that a response is returned.
        """
        data = {
            'text': 'How are you?'
        }
        response = self.client.post(
            self.api_url,
            data=json.dumps(data),
            content_type='application/json',
            format='json'
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn('text', str(response.content))
        self.assertIn('in_response_to', str(response.content))

    def test_post_extra_data(self):
        post_data = {
            'text': 'Good morning.',
            'extra_data': {
                'user': 'jen@example.com'
            }
        }
        response = self.client.post(
            self.api_url,
            data=json.dumps(post_data),
            content_type='application/json',
            format='json'
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn('text', str(response.content))
        self.assertIn('extra_data', str(response.content))
        self.assertIn('in_response_to', str(response.content))


class ApiIntegrationTestCase(TestCase):
    """
    Test to make sure the ChatterBot API view works
    properly with the example Django app.
    """

    def setUp(self):
        super(ApiIntegrationTestCase, self).setUp()
        self.api_url = reverse('chatterbot:chatterbot')

        # Clear the response queue before tests
        ChatterBotView.chatterbot.conversation_sessions.get(
            ChatterBotView.chatterbot.default_session.id_string
        ).conversation.flush()

    def tearDown(self):
        super(ApiIntegrationTestCase, self).tearDown()

        # Clear the response queue after tests
        ChatterBotView.chatterbot.conversation_sessions.get(
            ChatterBotView.chatterbot.default_session.id_string
        ).conversation.flush()

    def _get_json(self, response):
        return json.loads(force_text(response.content))

    def test_get_conversation_empty(self):
        response = self.client.get(self.api_url)
        data = self._get_json(response)

        self.assertIn('conversation', data)
        self.assertEqual(len(data['conversation']), 0)

    def test_get_conversation(self):
        response = self.client.post(
            self.api_url,
            data=json.dumps({'text': 'How are you?'}),
            content_type='application/json',
            format='json'
        )

        response = self.client.get(self.api_url)
        data = self._get_json(response)

        self.assertIn('conversation', data)
        self.assertEqual(len(data['conversation']), 1)
        self.assertEqual(len(data['conversation'][0]), 2)
        self.assertIn('text', data['conversation'][0][0])
        self.assertIn('text', data['conversation'][0][1])
