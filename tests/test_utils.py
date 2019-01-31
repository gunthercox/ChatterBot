from tests.base_case import ChatBotTestCase
from unittest import TestCase
from chatterbot import utils


class UtilityTests(TestCase):

    def test_import_module(self):
        datetime = utils.import_module('datetime.datetime')
        self.assertTrue(hasattr(datetime, 'now'))

    def test_nltk_download_corpus(self):
        downloaded = utils.nltk_download_corpus('wordnet')
        self.assertTrue(downloaded)

    def test_treebank_to_wordnet(self):
        self.assertEqual(utils.treebank_to_wordnet('NNS'), 'n')

    def test_treebank_to_wordnet_no_match(self):
        self.assertEqual(utils.treebank_to_wordnet('XXX'), None)


class UtilityChatBotTestCase(ChatBotTestCase):

    def test_get_response_time(self):
        """
        Test that a response time is returned.
        """

        response_time = utils.get_response_time(self.chatbot)

        self.assertGreater(response_time, 0)
