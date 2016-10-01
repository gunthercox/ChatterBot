from django.test import TestCase
from django.core.urlresolvers import reverse


class ApiTestCase(TestCase):

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
        response = self.client.post(self.api_url, data, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertIn('text', str(response.content))
        self.assertIn('in_response_to', str(response.content))

    def test_get(self):
        response = self.client.get(self.api_url)

        self.assertEqual(response.status_code, 405)

    def test_patch(self):
        response = self.client.patch(self.api_url)

        self.assertEqual(response.status_code, 405)

    def test_delete(self):
        response = self.client.delete(self.api_url)

        self.assertEqual(response.status_code, 405)
