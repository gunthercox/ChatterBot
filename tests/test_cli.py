from unittest import TestCase
from chatterbot import __version__
from chatterbot import __main__ as main


class CommandLineInterfaceTests(TestCase):
    """
    Tests for the command line tools that are included with ChatterBot.
    """

    def test_get_chatterbot_version(self):
        version = main.get_chatterbot_version()
        self.assertEqual(version, __version__)

    def test_get_nltk_data_directories(self):
        directories = main.get_nltk_data_directories()
        self.assertIn('/', directories)
