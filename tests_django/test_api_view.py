import json
from django.test import TestCase
from django.core.urlresolvers import reverse


class ApiIntegrationTestCase(TestCase):

    def setUp(self):
        super(ApiIntegrationTestCase, self).setUp()
        self.api_url = reverse('chatterbot')

    def _get_json(self, response):
        from django.utils.encoding import force_text
        return json.loads(force_text(response.content))

    def test_get_conversation_empty(self):
        response = self.client.get(self.api_url)
        data = self._get_json(response)

        self.assertIn('conversation', data)
        self.assertEqual(len(data['conversation']), 0)

    def test_get_conversation(self):
        self.client.post(
            self.api_url,
            data=json.dumps({'text': 'How are you?'}),
            content_type='application/json',
            format='json'
        )

        response = self.client.get(self.api_url)
        data = self._get_json(response)

        self.assertIn('conversation', data)
        self.assertEqual(len(data['conversation']), 2)
        self.assertIn('text', data['conversation'][0])
        self.assertIn('text', data['conversation'][1])
