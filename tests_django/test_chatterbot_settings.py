from django.test import TestCase
from django.conf import settings


class SettingsTestCase(TestCase):

    def test_modified_settings(self):
        with self.settings(CHATTERBOT={'name': 'Jim'}):
            self.assertIn('name', settings.CHATTERBOT)
            self.assertEqual('Jim', settings.CHATTERBOT['name'])

    def test_name_setting(self):
        from django.core.urlresolvers import reverse

        api_url = reverse('chatterbot')
        response = self.client.get(api_url)

        self.assertEqual(response.status_code, 405)
        self.assertIn('detail', str(response.content))
        self.assertIn('name', str(response.content))
        self.assertIn('Test Django ChatterBot', str(response.content))
