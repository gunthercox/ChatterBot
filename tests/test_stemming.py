from unittest import TestCase
from chatterbot import stemming


class StemmerTests(TestCase):

    def setUp(self):
        self.stemmer = stemming.SimpleStemmer()

    def test_stemming(self):
        stemmed_text = self.stemmer.stem('Hello, how are you doing on this awesome day?')

        self.assertEqual(stemmed_text, 'ell wesom')

    def test_string_becomes_lowercase(self):
        stemmed_text = self.stemmer.stem('THIS IS HOW IT BEGINS!')

        self.assertEqual(stemmed_text, 'egin')

    def test_stemming_medium_sized_words(self):
        stemmed_text = self.stemmer.stem('Hello, my name is Gunther.')

        self.assertEqual(stemmed_text, 'ell am unthe')

    def test_stemming_long_words(self):
        stemmed_text = self.stemmer.stem('I play several orchestra instruments for pleasuer.')

        self.assertEqual(stemmed_text, 'la evera chest strumen easu')

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
