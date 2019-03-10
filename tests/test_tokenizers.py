from unittest import TestCase
from chatterbot import languages
from chatterbot.tokenizers import get_sentence_tokenizer, get_word_tokenizer


class EnglishSentenceTokenizerTests(TestCase):

    def setUp(self):
        super().setUp()

        self.tokenizer = get_sentence_tokenizer(languages.ENG)

    def test_one_sentence(self):
        tokens = self.tokenizer.tokenize('Hello, how are you?')

        self.assertEqual(len(tokens), 1)
        self.assertIn('Hello, how are you?', tokens)

    def test_two_sentences(self):
        tokens = self.tokenizer.tokenize('It is so nice out. Don\'t you think so?')

        self.assertEqual(len(tokens), 2)
        self.assertIn('It is so nice out.', tokens)
        self.assertIn('Don\'t you think so?', tokens)


class EnglishWordTokenizerTests(TestCase):

    def setUp(self):
        super().setUp()

        self.tokenizer = get_word_tokenizer(languages.ENG)

    def test_one_sentence(self):
        tokens = self.tokenizer.tokenize('Hello, how are you?')

        self.assertEqual(['Hello', ',', 'how', 'are', 'you', '?'], tokens)
