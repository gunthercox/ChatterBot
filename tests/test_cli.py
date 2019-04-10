from unittest import TestCase
from chatterbot import __main__ as main


class CommandLineInterfaceTests(TestCase):
    """
    Tests for the command line tools that are included with ChatterBot.
    """

    def test_get_chatterbot_version(self):
        version = main.get_chatterbot_version()
        version_parts = version.split('.')
        self.assertEqual(len(version_parts), 3)
        self.assertTrue(version_parts[0].isdigit())
        self.assertTrue(version_parts[1].isdigit())
