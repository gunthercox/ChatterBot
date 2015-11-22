from unittest import TestCase
from chatterbot.corpus import Corpus
import os


class CorpusUtilsTestCase(TestCase):

    def setUp(self):
        self.corpus = Corpus()

    def test_get_file_path(self):
        """
        Test that a dotted path is properly converted to a file address.
        """
        path = self.corpus.get_file_path("chatterbot.corpus.english")
        self.assertIn(
            os.path.join("chatterbot", "corpus", "data", "english"),
            path
        )

    def test_read_corpus(self):
        corpus_path = os.path.join(
            self.corpus.data_directory,
            "english", "conversations.json"
        )
        data = self.corpus.read_corpus(corpus_path)
        self.assertIn("conversations", data)

    def test_load_corpus(self):
        corpus = self.corpus.load_corpus("chatterbot.corpus.english.greetings")

        self.assertEqual(len(corpus), 1)
        self.assertIn(["Hi", "Hello"], corpus[0])

    def test_load_corpus_general(self):
        corpus = self.corpus.load_corpus("chatterbot.corpus.english")

        self.assertEqual(len(corpus), 3)
        self.assertIn(["Hi", "Hello"], corpus[1])

