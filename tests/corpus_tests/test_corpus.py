from unittest import TestCase
from chatterbot.corpus.utils import read_corpus, load_corpus


class CorpusUtilsTestCase(TestCase):

    def test_read_corpus(self):
        #data = read_corpus("chatterbot/corpus/english/greetings/conversations.json")
        # TODO
        pass

    def test_load_corpus(self):
        corpus = load_corpus("chatterbot.corpus.english.greetings")

        self.assertEqual(len(corpus), 1)
        self.assertIn(["Hi", "Hello"], corpus[0])

    def test_load_corpus_general(self):
        corpus = load_corpus("chatterbot.corpus.english")

        self.assertEqual(len(corpus), 2)
        self.assertIn(["Hi", "Hello"], corpus[0])

