# -*- coding: utf-8 -*-
from unittest import TestCase
from chatterbot import utils


class UtilityTests(TestCase):

    def test_import_module(self):
        datetime = utils.import_module('datetime.datetime')
        self.assertTrue(hasattr(datetime, 'now'))

    def test_nltk_download_corpus(self):
        downloaded = utils.nltk_download_corpus('wordnet')
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
