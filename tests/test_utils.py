# -*- coding: utf-8 -*-
from unittest import TestCase
from chatterbot.utils.clean import clean_whitespace
from chatterbot.utils.clean import clean
from chatterbot.utils.module_loading import import_module


class UtilityTests(TestCase):

    def test_import_module(self):
        datetime = import_module('datetime.datetime')
        self.assertTrue(hasattr(datetime, 'now'))


class TokenizerTestCase(TestCase):

    def setUp(self):
        super(TokenizerTestCase, self).setUp()
        from chatterbot.utils.tokenizer import Tokenizer

        self.tokenizer = Tokenizer()

    def test_get_tokens(self):
        tokens = self.tokenizer.get_tokens('what time is it', exclude_stop_words=False)
        self.assertEqual(tokens, ['what', 'time', 'is', 'it'])

    def test_get_tokens_exclude_stop_words(self):
        tokens = self.tokenizer.get_tokens('what time is it', exclude_stop_words=True)
        self.assertEqual(tokens, {'time'})


class StopWordsTestCase(TestCase):

    def setUp(self):
        super(StopWordsTestCase, self).setUp()
        from chatterbot.utils.stop_words import StopWordsManager

        self.stopwords_manager = StopWordsManager()

    def test_remove_stop_words(self):
        tokens = ['this', 'is', 'a', 'test', 'string']
        words = self.stopwords_manager.remove_stopwords('english', tokens)

        # This example list of words should end up with only two elements
        self.assertEqual(len(words), 2)
        self.assertIn('test', list(words))
        self.assertIn('string', list(words))


class WordnetTestCase(TestCase):

    def setUp(self):
        super(WordnetTestCase, self).setUp()
        from chatterbot.utils.wordnet import Wordnet

        self.wordnet = Wordnet()

    def test_wordnet(self):
        synsets = self.wordnet.synsets('test')

        self.assertEqual(
            0.06666666666666667,
            synsets[0].path_similarity(synsets[1])
        )


class CleanWhitespaceTests(TestCase):

    def test_clean_whitespace(self):
        text = '\tThe quick \nbrown fox \rjumps over \vthe \alazy \fdog\\.'
        clean_text = clean_whitespace(text)
        normal_text = 'The quick brown fox jumps over \vthe \alazy \fdog\\.'

        self.assertEqual(clean_text, normal_text)

    def test_leading_or_trailing_whitespace_removed(self):

        text = '     The quick brown fox jumps over the lazy dog.   '
        clean_text = clean_whitespace(text)
        normal_text = 'The quick brown fox jumps over the lazy dog.'

        self.assertEqual(clean_text, normal_text)

    def test_consecutive_spaces_removed(self):

        text = 'The       quick brown     fox      jumps over the lazy dog.'
        clean_text = clean_whitespace(text)
        normal_text = 'The quick brown fox jumps over the lazy dog.'

        self.assertEqual(clean_text, normal_text)


class CleanTests(TestCase):

    def test_html_characters_restored(self):

        # implicit concatenation
        text = 'The quick brown fox &lt;b&gt;jumps&lt;/b&gt; over'
        ' the <a href="http://lazy.com">lazy</a> dog.'

        normal_text = 'The quick brown fox <b>jumps</b> over'
        ' the <a href="http://lazy.com">lazy</a> dog.'

        clean_text = clean(text)

        self.assertEqual(clean_text, normal_text)

    def test_non_ascii_chars_replaced(self):

        text = u"Klüft skräms inför på fédéral électoral große"
        clean_text = clean(text)
        normal_text = "Kluft skrams infor pa federal electoral groe"

        self.assertEqual(clean_text, normal_text)
