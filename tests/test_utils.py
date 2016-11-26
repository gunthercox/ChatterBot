# -*- coding: utf-8 -*-
from unittest import TestCase
from chatterbot import utils


class UtilityTests(TestCase):

    def test_import_module(self):
        datetime = utils.import_module('datetime.datetime')
        self.assertTrue(hasattr(datetime, 'now'))


class CleanWhitespaceTests(TestCase):

    def test_clean_whitespace(self):
        text = '\tThe quick \nbrown fox \rjumps over \vthe \alazy \fdog\\.'
        clean_text = utils.clean_whitespace(text)
        normal_text = 'The quick brown fox jumps over \vthe \alazy \fdog\\.'

        self.assertEqual(clean_text, normal_text)

    def test_leading_or_trailing_whitespace_removed(self):

        text = '     The quick brown fox jumps over the lazy dog.   '
        clean_text = utils.clean_whitespace(text)
        normal_text = 'The quick brown fox jumps over the lazy dog.'

        self.assertEqual(clean_text, normal_text)

    def test_consecutive_spaces_removed(self):

        text = 'The       quick brown     fox      jumps over the lazy dog.'
        clean_text = utils.clean_whitespace(text)
        normal_text = 'The quick brown fox jumps over the lazy dog.'

        self.assertEqual(clean_text, normal_text)


class CleanTests(TestCase):

    def test_html_characters_restored(self):

        # implicit concatenation
        text = 'The quick brown fox &lt;b&gt;jumps&lt;/b&gt; over'
        ' the <a href="http://lazy.com">lazy</a> dog.'

        normal_text = 'The quick brown fox <b>jumps</b> over'
        ' the <a href="http://lazy.com">lazy</a> dog.'

        clean_text = utils.clean(text)

        self.assertEqual(clean_text, normal_text)

    def test_non_ascii_chars_replaced(self):

        text = u"Klüft skräms inför på fédéral électoral große"
        clean_text = utils.clean(text)
        normal_text = "Kluft skrams infor pa federal electoral groe"

        self.assertEqual(clean_text, normal_text)
