from django.test import TestCase
from django.core.urlresolvers import reverse


class ApiTestCase(TestCase):

    def test_post(self):
        """
        Test that a response is returned.
        """
        data = {
            'text': 'How are you?'
        }
        api_url = reverse('chatterbot:chatterbot')
        response = self.client.post(api_url, data, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertIn('text', str(response.content))
        self.assertIn('in_response_to', str(response.content))
