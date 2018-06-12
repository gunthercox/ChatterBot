from django.test import TestCase
from django.conf import settings


class SettingsTestCase(TestCase):

    def test_modified_settings(self):
        with self.settings(CHATTERBOT={'name': 'Jim'}):
            self.assertIn('name', settings.CHATTERBOT)
            self.assertEqual('Jim', settings.CHATTERBOT['name'])

    def test_name_setting(self):
        with self.settings():
            self.assertIn('name', settings.CHATTERBOT)
            self.assertEqual('Test Django ChatterBot', settings.CHATTERBOT['name'])
