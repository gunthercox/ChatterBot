import json
from django.test import TestCase
from django.urls import reverse


class ViewTestCase(TestCase):

    def setUp(self):
        super().setUp()
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
        super().setUp()
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


class ApiIntegrationTestCase(TestCase):
    """
    Test to make sure the ChatterBot API view works
    properly with the example Django app.
    """

    def setUp(self):
        super().setUp()
        self.api_url = reverse('chatterbot')

    def test_get(self):
        response = self.client.get(self.api_url)

        self.assertIn('name', response.json())
