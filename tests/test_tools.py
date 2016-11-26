from unittest import TestCase


class TokenizerTestCase(TestCase):

    def setUp(self):
        super(TokenizerTestCase, self).setUp()
        from chatterbot.tools.tokenizer import Tokenizer

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
        from chatterbot.tools.stop_words import StopWordsManager

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
        from chatterbot.tools.wordnet import Wordnet

        self.wordnet = Wordnet()

    def test_wordnet(self):
        synsets = self.wordnet.synsets('test')

        self.assertEqual(
            0.06666666666666667,
            synsets[0].path_similarity(synsets[1])
        )
