from unittest import TestCase
from chatterbot import languages
from chatterbot import tagging
from chatterbot import utils


class PosLemmaTaggerTests(TestCase):

    def setUp(self):
        self.tagger = tagging.PosLemmaTagger()

    def test_empty_string(self):
        tagged_text = self.tagger.get_bigram_pair_string(
            ''
        )

        self.assertEqual(tagged_text, '')

    def test_tagging(self):
        tagged_text = self.tagger.get_bigram_pair_string(
            'Hello, how are you doing on this awesome day?'
        )

        self.assertEqual(tagged_text, 'INTJ:awesome ADJ:day')

    def test_tagging_english(self):
        self.tagger = tagging.PosLemmaTagger(
            language=languages.ENG
        )

        tagged_text = self.tagger.get_bigram_pair_string(
            'Hello, how are you doing on this awesome day?'
        )

        self.assertEqual(tagged_text, 'INTJ:awesome ADJ:day')

    def test_tagging_german(self):
        self.tagger = tagging.PosLemmaTagger(
            language=languages.GER
        )

        tagged_text = self.tagger.get_bigram_pair_string(
            'Ich spreche nicht viel Deutsch.'
        )

        self.assertEqual(tagged_text, 'VERB:deutsch')

    def test_string_becomes_lowercase(self):
        tagged_text = self.tagger.get_bigram_pair_string('THIS IS HOW IT BEGINS!')

        self.assertEqual(tagged_text, 'DET:be VERB:how ADV:it NOUN:begin')

    def test_tagging_medium_sized_words(self):
        tagged_text = self.tagger.get_bigram_pair_string('Hello, my name is Gunther.')

        self.assertEqual(tagged_text, 'INTJ:gunther')

    def test_tagging_long_words(self):
        tagged_text = self.tagger.get_bigram_pair_string('I play several orchestra instruments for pleasure.')

        self.assertEqual(tagged_text, 'VERB:orchestra ADJ:instrument NOUN:pleasure')

    def test_get_bigram_pair_string_punctuation_only(self):
        bigram_string = self.tagger.get_bigram_pair_string(
            '?'
        )

        self.assertEqual(bigram_string, '?')

    def test_get_bigram_pair_string_single_character(self):
        bigram_string = self.tagger.get_bigram_pair_string(
            '🙂'
        )

        self.assertEqual(bigram_string, '🙂')

    def test_get_bigram_pair_string_single_character_punctuated(self):
        bigram_string = self.tagger.get_bigram_pair_string(
            '🤷?'
        )

        self.assertEqual(bigram_string, '🤷')

    def test_get_bigram_pair_string_two_characters(self):
        bigram_string = self.tagger.get_bigram_pair_string(
            'AB'
        )

        self.assertEqual(bigram_string, 'ab')

    def test_get_bigram_pair_string_three_characters(self):
        bigram_string = self.tagger.get_bigram_pair_string(
            'ABC'
        )

        self.assertEqual(bigram_string, 'abc')

    def test_get_bigram_pair_string_four_characters(self):
        bigram_string = self.tagger.get_bigram_pair_string(
            'ABCD'
        )

        self.assertEqual(bigram_string, 'abcd')

    def test_get_bigram_pair_string_five_characters(self):
        bigram_string = self.tagger.get_bigram_pair_string(
            'ABCDE'
        )

        self.assertEqual(bigram_string, 'abcde')

    def test_get_bigram_pair_string_single_word(self):
        bigram_string = self.tagger.get_bigram_pair_string(
            'Hello'
        )

        self.assertEqual(bigram_string, 'hello')

    def test_get_bigram_pair_string_multiple_words(self):
        bigram_string = self.tagger.get_bigram_pair_string(
            'Hello Dr. Salazar. How are you today?'
        )

        self.assertEqual(bigram_string, 'INTJ:salazar PROPN:today')

    def test_get_bigram_pair_string_single_character_words(self):
        bigram_string = self.tagger.get_bigram_pair_string(
            'a e i o u'
        )

        self.assertEqual(bigram_string, 'NOUN:o NOUN:u')

    def test_get_bigram_pair_string_two_character_words(self):
        bigram_string = self.tagger.get_bigram_pair_string(
            'Lo my mu it is of us'
        )

        self.assertEqual(bigram_string, 'VERB:mu')


class PosHypernymTaggerTests(TestCase):

    def setUp(self):
        self.tagger = tagging.PosHypernymTagger()

        # Make sure the required NLTK data files are downloaded
        for function in utils.get_initialization_functions(self, 'tagger'):
            function()

    def test_empty_string(self):
        tagged_text = self.tagger.get_bigram_pair_string(
            ''
        )

        self.assertEqual(tagged_text, '')

    def test_tagging(self):
        tagged_text = self.tagger.get_bigram_pair_string(
            'Hello, how are you doing on this awesome day?'
        )

        self.assertEqual(tagged_text, 'DT:awesome JJ:time_unit')

    def test_tagging_english(self):
        self.tagger = tagging.PosHypernymTagger(
            language=languages.ENG
        )

        tagged_text = self.tagger.get_bigram_pair_string(
            'Hello, how are you doing on this awesome day?'
        )

        self.assertEqual(tagged_text, 'DT:awesome JJ:time_unit')

    def test_tagging_french(self):
        self.tagger = tagging.PosHypernymTagger(
            language=languages.FRE
        )

        tagged_text = self.tagger.get_bigram_pair_string(
            'Salut comment allez-vous?'
        )

        self.assertEqual(tagged_text, 's:comment c:allez-vous')

    def test_tagging_russian(self):
        self.tagger = tagging.PosHypernymTagger(
            language=languages.RUS
        )

        tagged_text = self.tagger.get_bigram_pair_string(
            'Привет, как ты?'
        )

        self.assertEqual(tagged_text, 'п:как к:ты')

    def test_string_becomes_lowercase(self):
        tagged_text = self.tagger.get_bigram_pair_string('THIS IS HOW IT BEGINS!')

        self.assertEqual(tagged_text, 'NNP:begins')

    def test_tagging_medium_sized_words(self):
        tagged_text = self.tagger.get_bigram_pair_string('Hello, my name is Gunther.')

        self.assertEqual(tagged_text, 'PRP$:language_unit VBZ:gunther')

    def test_tagging_long_words(self):
        tagged_text = self.tagger.get_bigram_pair_string('I play several orchestra instruments for pleasuer.')

        self.assertEqual(tagged_text, 'PRP:compete VBP:several JJ:orchestra JJ:device IN:pleasuer')

    def test_get_bigram_pair_string_punctuation_only(self):
        bigram_string = self.tagger.get_bigram_pair_string(
            '?'
        )

        self.assertEqual(bigram_string, '?')

    def test_get_bigram_pair_string_single_character(self):
        bigram_string = self.tagger.get_bigram_pair_string(
            '🙂'
        )

        self.assertEqual(bigram_string, '🙂')

    def test_get_bigram_pair_string_single_character_punctuated(self):
        bigram_string = self.tagger.get_bigram_pair_string(
            '🤷?'
        )

        self.assertEqual(bigram_string, '🤷')

    def test_get_bigram_pair_string_two_characters(self):
        bigram_string = self.tagger.get_bigram_pair_string(
            'AB'
        )

        self.assertEqual(bigram_string, 'ab')

    def test_get_bigram_pair_string_three_characters(self):
        bigram_string = self.tagger.get_bigram_pair_string(
            'ABC'
        )

        self.assertEqual(bigram_string, 'abc')

    def test_get_bigram_pair_string_four_characters(self):
        bigram_string = self.tagger.get_bigram_pair_string(
            'ABCD'
        )

        self.assertEqual(bigram_string, 'abcd')

    def test_get_bigram_pair_string_five_characters(self):
        bigram_string = self.tagger.get_bigram_pair_string(
            'ABCDE'
        )

        self.assertEqual(bigram_string, 'abcde')

    def test_get_bigram_pair_string_single_word(self):
        bigram_string = self.tagger.get_bigram_pair_string(
            'Hello'
        )

        self.assertEqual(bigram_string, 'hello')

    def test_get_bigram_pair_string_multiple_words(self):
        bigram_string = self.tagger.get_bigram_pair_string(
            'Hello Dr. Salazar. How are you today?'
        )

        self.assertEqual(bigram_string, 'NNP:scholar NNP:salazar PRP:present')

    def test_get_bigram_pair_string_single_character_words(self):
        bigram_string = self.tagger.get_bigram_pair_string(
            'a e i o u'
        )

        self.assertEqual(bigram_string, 'DT:e NN:i NN:o VBP:u')

    def test_get_bigram_pair_string_two_character_words(self):
        bigram_string = self.tagger.get_bigram_pair_string(
            'Lo my mu it is of us'
        )

        self.assertEqual(bigram_string, 'PRP$:letter IN:us')
