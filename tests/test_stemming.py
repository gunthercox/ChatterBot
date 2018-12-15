from unittest import TestCase
from chatterbot import stemming


class SimpleStemmerTests(TestCase):

    def setUp(self):
        self.stemmer = stemming.SimpleStemmer()

    def test_empty_string(self):
        stemmed_text = self.stemmer.get_bigram_pair_string(
            ''
        )

        self.assertEqual(stemmed_text, '')

    def test_stemming(self):
        stemmed_text = self.stemmer.get_stemmed_words(
            'Hello, how are you doing on this awesome day?'
        )

        self.assertEqual(stemmed_text, ['ell', 'wesom'])

    def test_string_becomes_lowercase(self):
        stemmed_text = self.stemmer.get_stemmed_words('THIS IS HOW IT BEGINS!')

        self.assertEqual(stemmed_text, ['egin'])

    def test_stemming_medium_sized_words(self):
        stemmed_text = self.stemmer.get_stemmed_words('Hello, my name is Gunther.')

        self.assertEqual(stemmed_text, ['ell', 'am', 'unthe'])

    def test_stemming_long_words(self):
        stemmed_text = self.stemmer.get_stemmed_words('I play several orchestra instruments for pleasuer.')

        self.assertEqual(stemmed_text, ['la', 'evera', 'chest', 'strumen', 'easu'])

    def test_get_bigram_pair_string_punctuation_only(self):
        bigram_string = self.stemmer.get_bigram_pair_string(
            '?'
        )

        self.assertEqual(bigram_string, '?')

    def test_get_bigram_pair_string_single_character(self):
        bigram_string = self.stemmer.get_bigram_pair_string(
            '🙂'
        )

        self.assertEqual(bigram_string, '🙂')

    def test_get_bigram_pair_string_single_character_punctuated(self):
        bigram_string = self.stemmer.get_bigram_pair_string(
            '🤷?'
        )

        self.assertEqual(bigram_string, '🤷')

    def test_get_bigram_pair_string_two_characters(self):
        bigram_string = self.stemmer.get_bigram_pair_string(
            'AB'
        )

        self.assertEqual(bigram_string, 'ab')

    def test_get_bigram_pair_string_three_characters(self):
        bigram_string = self.stemmer.get_bigram_pair_string(
            'ABC'
        )

        self.assertEqual(bigram_string, 'abc')

    def test_get_bigram_pair_string_four_characters(self):
        bigram_string = self.stemmer.get_bigram_pair_string(
            'ABCD'
        )

        self.assertEqual(bigram_string, 'bc')

    def test_get_bigram_pair_string_five_characters(self):
        bigram_string = self.stemmer.get_bigram_pair_string(
            'ABCDE'
        )

        self.assertEqual(bigram_string, 'bcd')

    def test_get_bigram_pair_string_single_word(self):
        bigram_string = self.stemmer.get_bigram_pair_string(
            'Hello'
        )

        self.assertEqual(bigram_string, 'ell')

    def test_get_bigram_pair_string_multiple_words(self):
        bigram_string = self.stemmer.get_bigram_pair_string(
            'Hello Dr. Salazar. How are you today?'
        )

        self.assertEqual(bigram_string, 'ellalaza alazaoda')

    def test_get_bigram_pair_string_single_character_words(self):
        bigram_string = self.stemmer.get_bigram_pair_string(
            'a e i o u'
        )

        self.assertEqual(bigram_string, 'ae ei io ou')

    def test_get_bigram_pair_string_two_character_words(self):
        bigram_string = self.stemmer.get_bigram_pair_string(
            'Lo my mu it is of us'
        )

        self.assertEqual(bigram_string, 'lomy mymu muit itis isof ofus')


class PosHypernymStemmerTests(TestCase):

    def setUp(self):
        self.stemmer = stemming.PosHypernymStemmer()

    def test_empty_string(self):
        stemmed_text = self.stemmer.get_bigram_pair_string(
            ''
        )

        self.assertEqual(stemmed_text, '')

    def test_stemming(self):
        stemmed_text = self.stemmer.get_bigram_pair_string(
            'Hello, how are you doing on this awesome day?'
        )

        self.assertEqual(stemmed_text, 'DT:awesome JJ:time_unit')

    def test_string_becomes_lowercase(self):
        stemmed_text = self.stemmer.get_bigram_pair_string('THIS IS HOW IT BEGINS!')

        self.assertEqual(stemmed_text, 'NNP:begins')

    def test_stemming_medium_sized_words(self):
        stemmed_text = self.stemmer.get_bigram_pair_string('Hello, my name is Gunther.')

        self.assertEqual(stemmed_text, 'PRP$:language_unit VBZ:gunther')

    def test_stemming_long_words(self):
        stemmed_text = self.stemmer.get_bigram_pair_string('I play several orchestra instruments for pleasuer.')

        self.assertEqual(stemmed_text, 'PRP:compete VBP:several JJ:orchestra JJ:device IN:pleasuer')

    def test_get_bigram_pair_string_punctuation_only(self):
        bigram_string = self.stemmer.get_bigram_pair_string(
            '?'
        )

        self.assertEqual(bigram_string, '?')

    def test_get_bigram_pair_string_single_character(self):
        bigram_string = self.stemmer.get_bigram_pair_string(
            '🙂'
        )

        self.assertEqual(bigram_string, '🙂')

    def test_get_bigram_pair_string_single_character_punctuated(self):
        bigram_string = self.stemmer.get_bigram_pair_string(
            '🤷?'
        )

        self.assertEqual(bigram_string, '🤷')

    def test_get_bigram_pair_string_two_characters(self):
        bigram_string = self.stemmer.get_bigram_pair_string(
            'AB'
        )

        self.assertEqual(bigram_string, 'ab')

    def test_get_bigram_pair_string_three_characters(self):
        bigram_string = self.stemmer.get_bigram_pair_string(
            'ABC'
        )

        self.assertEqual(bigram_string, 'abc')

    def test_get_bigram_pair_string_four_characters(self):
        bigram_string = self.stemmer.get_bigram_pair_string(
            'ABCD'
        )

        self.assertEqual(bigram_string, 'abcd')

    def test_get_bigram_pair_string_five_characters(self):
        bigram_string = self.stemmer.get_bigram_pair_string(
            'ABCDE'
        )

        self.assertEqual(bigram_string, 'abcde')

    def test_get_bigram_pair_string_single_word(self):
        bigram_string = self.stemmer.get_bigram_pair_string(
            'Hello'
        )

        self.assertEqual(bigram_string, 'hello')

    def test_get_bigram_pair_string_multiple_words(self):
        bigram_string = self.stemmer.get_bigram_pair_string(
            'Hello Dr. Salazar. How are you today?'
        )

        self.assertEqual(bigram_string, 'NNP:scholar NNP:salazar PRP:present')

    def test_get_bigram_pair_string_single_character_words(self):
        bigram_string = self.stemmer.get_bigram_pair_string(
            'a e i o u'
        )

        self.assertEqual(bigram_string, 'DT:e NN:i NN:o VBP:u')

    def test_get_bigram_pair_string_two_character_words(self):
        bigram_string = self.stemmer.get_bigram_pair_string(
            'Lo my mu it is of us'
        )

        self.assertEqual(bigram_string, 'PRP$:letter IN:us')
