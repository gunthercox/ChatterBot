from unittest import TestCase
from chatterbot import languages
from chatterbot import tagging


class PosLemmaTaggerTests(TestCase):

    def setUp(self):
        self.tagger = tagging.PosLemmaTagger()

    def test_empty_string(self):
        tagged_text = self.tagger.get_text_index_string(
            ''
        )

        self.assertEqual(tagged_text, '')

    def test_tagging(self):
        tagged_text = self.tagger.get_text_index_string(
            'Hello, how are you doing on this awesome day?'
        )

        self.assertEqual(tagged_text, 'INTJ:awesome ADJ:day')

    def test_tagging_english(self):
        self.tagger = tagging.PosLemmaTagger(
            language=languages.ENG
        )

        tagged_text = self.tagger.get_text_index_string(
            'Hello, how are you doing on this awesome day?'
        )

        self.assertEqual(tagged_text, 'INTJ:awesome ADJ:day')

    def test_tagging_german(self):
        self.tagger = tagging.PosLemmaTagger(
            language=languages.GER
        )

        tagged_text = self.tagger.get_text_index_string(
            'Ich spreche nicht viel Deutsch.'
        )

        self.assertEqual(tagged_text, 'VERB:deutsch')

    def test_string_becomes_lowercase(self):
        tagged_text = self.tagger.get_text_index_string('THIS IS HOW IT BEGINS!')

        self.assertEqual(tagged_text, 'DET:be VERB:how ADV:it NOUN:begin')

    def test_tagging_medium_sized_words(self):
        tagged_text = self.tagger.get_text_index_string('Hello, my name is Gunther.')

        self.assertEqual(tagged_text, 'INTJ:gunther')

    def test_tagging_long_words(self):
        tagged_text = self.tagger.get_text_index_string('I play several orchestra instruments for pleasure.')

        self.assertEqual(tagged_text, 'VERB:orchestra ADJ:instrument NOUN:pleasure')

    def test_get_text_index_string_punctuation_only(self):
        bigram_string = self.tagger.get_text_index_string(
            '?'
        )

        self.assertEqual(bigram_string, '?')

    def test_get_text_index_string_single_character(self):
        bigram_string = self.tagger.get_text_index_string(
            '🙂'
        )

        self.assertEqual(bigram_string, '🙂')

    def test_get_text_index_string_single_character_punctuated(self):
        bigram_string = self.tagger.get_text_index_string(
            '🤷?'
        )

        self.assertEqual(bigram_string, '🤷')

    def test_get_text_index_string_two_characters(self):
        bigram_string = self.tagger.get_text_index_string(
            'AB'
        )

        self.assertEqual(bigram_string, 'ab')

    def test_get_text_index_string_three_characters(self):
        bigram_string = self.tagger.get_text_index_string(
            'ABC'
        )

        self.assertEqual(bigram_string, 'abc')

    def test_get_text_index_string_four_characters(self):
        bigram_string = self.tagger.get_text_index_string(
            'ABCD'
        )

        self.assertEqual(bigram_string, 'abcd')

    def test_get_text_index_string_five_characters(self):
        bigram_string = self.tagger.get_text_index_string(
            'ABCDE'
        )

        self.assertEqual(bigram_string, 'abcde')

    def test_get_text_index_string_single_word(self):
        bigram_string = self.tagger.get_text_index_string(
            'Hello'
        )

        self.assertEqual(bigram_string, 'hello')

    def test_get_text_index_string_multiple_words(self):
        bigram_string = self.tagger.get_text_index_string(
            'Hello Dr. Salazar. How are you today?'
        )

        self.assertEqual(bigram_string, 'INTJ:salazar PROPN:today')

    def test_get_text_index_string_single_character_words(self):
        bigram_string = self.tagger.get_text_index_string(
            'a e i o u'
        )

        self.assertEqual(bigram_string, 'NOUN:o NOUN:u')

    def test_get_text_index_string_two_character_words(self):
        bigram_string = self.tagger.get_text_index_string(
            'Lo my mu it is of us'
        )

        self.assertEqual(bigram_string, 'VERB:mu')
