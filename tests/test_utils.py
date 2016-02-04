# -*- coding: utf-8 -*-
from unittest import TestCase

from chatterbot.utils.clean import clean_whitespace
from chatterbot.utils.clean import clean
from chatterbot.utils.module_loading import import_module
from chatterbot.utils.pos_tagger import POSTagger
from chatterbot.utils.stop_words import StopWordsManager
from chatterbot.utils.word_net import Wordnet
from chatterbot.utils.entity_tagger import NamedEntityTagger


class UtilityTests(TestCase):

    def test_import_module(self):
        datetime = import_module("datetime.datetime")
        self.assertTrue(hasattr(datetime, 'now'))

    def test_pos_tagger(self):
        pos_tagger = POSTagger()
        tokens = pos_tagger.tokenize("what time is it")

        self.assertEqual(tokens, ['what', 'time', 'is', 'it'])

    def test_stop_words(self):
        stopwords_manager = StopWordsManager()
        words = stopwords_manager.words("english")
        test_case = set(["too"]) - set(words)

        self.assertEqual(test_case, set([]))

    def test_word_net(self):
        wordnet = Wordnet()
        synsets = wordnet.synsets('test')

        self.assertEqual(0.06666666666666667, synsets[0].path_similarity(synsets[1]))

    def test_ne_tagger(self):
        named_entity_tagger = NamedEntityTagger()
        named_entities = named_entity_tagger.ne_chunk("test one, two, and three.")
        valid_check = named_entity_tagger.ne_chunk("New York Times")

        self.assertEqual(named_entities, [])
        self.assertEqual(valid_check, ['New', 'York', 'Times'])

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
