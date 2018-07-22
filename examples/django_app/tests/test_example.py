import json
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.utils.encoding import force_text


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
        self.api_url = reverse('chatterbot')

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
        self.api_url = reverse('chatterbot')

    def _get_json(self, response):
        return json.loads(force_text(response.content))

    def test_get(self):
        response = self.client.get(self.api_url)
        data = self._get_json(response)

        self.assertIn('name', data)
