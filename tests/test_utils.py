# -*- coding: utf-8 -*-
from .base_case import ChatBotTestCase
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

    def test_generate_strings(self):
        """
        Test that we can generate 2 strings of length 10.
        """
        strings = utils.generate_strings(2, 10)
        self.assertEqual(len(strings), 2)
        self.assertEqual(len(strings[0]), 10)
        self.assertEqual(len(strings[1]), 10)


class UtilityChatBotTestCase(ChatBotTestCase):

    def test_get_response_time(self):
        """
        Test that a response time is returned.
        """

        response_time = utils.get_response_time(self.chatbot)

        self.assertGreater(response_time, 0)
