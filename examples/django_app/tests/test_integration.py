from django.test import TestCase
from django.core.urlresolvers import reverse
from django.utils.encoding import force_text
from chatterbot.ext.django_chatterbot.views import ChatterBotView
import unittest
import json


class ApiIntegrationTestCase(TestCase):

    def setUp(self):
        super(ApiIntegrationTestCase, self).setUp()
        self.api_url = reverse('chatterbot:chatterbot')

        # Clear the response queue before tests
        ChatterBotView.chatterbot.recent_statements.flush()

    def tearDown(self):
        super(ApiIntegrationTestCase, self).tearDown()

        # Clear the response queue after tests
        ChatterBotView.chatterbot.recent_statements.flush()

    def _get_json(self, response):
        return json.loads(force_text(response.content))

    def test_get_recent_statements_empty(self):
        response = self.client.get(self.api_url)
        data = self._get_json(response)

        self.assertIn('recent_statements', data)
        self.assertEqual(len(data['recent_statements']), 0)

    def test_get_recent_statements(self):
        response = self.client.post(
            self.api_url,
            data=json.dumps({'text': 'How are you?'}),
            content_type='application/json',
            format='json'
        )

        response = self.client.get(self.api_url)
        data = self._get_json(response)

        self.assertIn('recent_statements', data)
        self.assertEqual(len(data['recent_statements']), 1)
        self.assertEqual(len(data['recent_statements'][0]), 2)
        self.assertIn('text', data['recent_statements'][0][0])
        self.assertIn('text', data['recent_statements'][0][1])
