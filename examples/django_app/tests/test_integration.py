from django.test import TestCase
from django.core.urlresolvers import reverse
import unittest


class ApiIntegrationTestCase(TestCase):

    def setUp(self):
        super(ApiIntegrationTestCase, self).setUp()
        self.api_url = reverse('chatterbot:chatterbot')

    def tearDown(self):
        super(ApiIntegrationTestCase, self).tearDown()
        from chatterbot.ext.django_chatterbot.views import ChatterBotView

        # Clear the response queue between tests
        ChatterBotView.chatterbot.recent_statements.queue = []

    def _get_json(self, response):
        import json
        return json.loads(str(response.content))

    def test_get_recent_statements_empty(self):
        response = self.client.get(self.api_url)
        data = self._get_json(response)

        self.assertIn('recent_statements', data)
        self.assertEqual(len(data['recent_statements']), 0)

    def test_get_recent_statements(self):
        response = self.client.post(
            self.api_url,
            {'text': 'How are you?'},
            format='json'
        )

        response = self.client.get(self.api_url)
        data = self._get_json(response)

        self.assertIn('recent_statements', data)
        self.assertEqual(len(data['recent_statements']), 1)
        self.assertEqual(len(data['recent_statements'][0]), 2)
        self.assertIn('text', data['recent_statements'][0][0])
        self.assertIn('text', data['recent_statements'][0][1])
