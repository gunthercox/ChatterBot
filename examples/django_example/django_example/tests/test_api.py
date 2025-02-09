import json
from django.test import TestCase
from django.urls import reverse


class ApiTestCase(TestCase):

    def setUp(self):
        super().setUp()
        self.api_url = reverse('chatterbot')

    def test_invalid_text(self):
        response = self.client.post(
            self.api_url,
            data=json.dumps({
                'type': 'classmethod'
            }),
            content_type='application/json',
            format='json'
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn('text', response.json())
        self.assertEqual(['The attribute "text" is required.'], response.json()['text'])

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

        self.assertEqual(response.status_code, 200)
        self.assertIn('text', response.json())
        self.assertGreater(len(response.json()['text']), 1)
        self.assertIn('in_response_to', response.json())

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

        self.assertEqual(response.status_code, 200)
        self.assertIn('text', response.json())
        self.assertGreater(len(response.json()['text']), 1)
        self.assertIn('in_response_to', response.json())

    def test_escaped_unicode_post(self):
        """
        Test that unicode reponce
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
        self.assertIn('text', response.json())
        self.assertIn('in_response_to', response.json())

    def test_post_tags(self):
        post_data = {
            'text': 'Good morning.',
            'tags': [
                'user:jen@example.com'
            ]
        }
        response = self.client.post(
            self.api_url,
            data=json.dumps(post_data),
            content_type='application/json',
            format='json'
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn('text', response.json())
        self.assertIn('in_response_to', response.json())
        self.assertIn('tags', response.json())
        self.assertEqual(response.json()['tags'], [])

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
