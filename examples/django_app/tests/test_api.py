# -*- coding: utf-8 -*-
import json
from django.test import TestCase
from django.core.urlresolvers import reverse


class ApiTestCase(TestCase):

    def setUp(self):
        super(ApiTestCase, self).setUp()
        self.api_url = reverse('chatterbot')

    def _get_json(self, response):
        from django.utils.encoding import force_text
        return json.loads(force_text(response.content))

    def test_invalid_text(self):
        response = self.client.post(
            self.api_url,
            data=json.dumps({
                'type': 'classmethod'
            }),
            content_type='application/json',
            format='json'
        )

        content = json.loads(response.content.decode('utf-8'))

        self.assertEqual(response.status_code, 400)
        self.assertIn('text', content)
        self.assertEqual(['The attribute "text" is required.'], content['text'])

    def test_post(self):
        """
        Test that a response is returned.
        """
        response = self.client.post(
            self.api_url,
            data=json.dumps({
                'text': 'How are you?'
            }),
            content_type='application/json',
            format='json'
        )

        content = json.loads(response.content.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        self.assertIn('text', content)
        self.assertGreater(len(content['text']), 1)
        self.assertIn('in_response_to', content)

    def test_post_unicode(self):
        """
        Test that a response is returned.
        """
        response = self.client.post(
            self.api_url,
            data=json.dumps({
                'text': u'سلام'
            }),
            content_type='application/json',
            format='json'
        )

        content = json.loads(response.content.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        self.assertIn('text', content)
        self.assertGreater(len(content['text']), 1)
        self.assertIn('in_response_to', content)

    def test_escaped_unicode_post(self):
        """
        Test that unicode reponse
        """
        response = self.client.post(
            self.api_url,
            data=json.dumps({
                'text': '\u2013'
            }),
            content_type='application/json',
            format=json
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

    def test_get(self):
        response = self.client.get(self.api_url)

        self.assertEqual(response.status_code, 200)

    def test_patch(self):
        response = self.client.patch(self.api_url)

        self.assertEqual(response.status_code, 405)

    def test_put(self):
        response = self.client.put(self.api_url)

        self.assertEqual(response.status_code, 405)

    def test_delete(self):
        response = self.client.delete(self.api_url)

        self.assertEqual(response.status_code, 405)
