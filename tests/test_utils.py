# -*- coding: utf-8 -*-
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
        self.skipTest('Test needs to be created')

    def test_remove_stop_words(self):
        from chatterbot.utils import nltk_download_corpus

        nltk_download_corpus('stopwords')

        tokens = ['this', 'is', 'a', 'test', 'string']
        words = utils.remove_stopwords(tokens, 'english')

        # This example list of words should end up with only two elements
        self.assertEqual(len(words), 2)
        self.assertIn('test', list(words))
        self.assertIn('string', list(words))

    def test_get_greatest_confidence(self):
        statement = 'Hello'
        options = [
            (0.50, 'Hello'),
            (0.85, 'Hello'),
            (0.42, 'Hello')
        ]
        value = utils.get_greatest_confidence(statement, options)

        self.assertEqual(value, 0.85)


class UtilityChatBotTestCase(ChatBotTestCase):

    def test_get_response_time(self):
        """
        Test that a response time is returned.
        """

        response_time = utils.get_response_time(self.chatbot)

        self.assertGreater(response_time, 0)
