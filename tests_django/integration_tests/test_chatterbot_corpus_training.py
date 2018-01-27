from django.test import TestCase
from django.conf import settings
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer


class ChatterBotCorpusTrainingTestCase(TestCase):
    """
    Test case for training with data from the ChatterBot Corpus.

    Note: This class has a mirror tests/training_tests/
    """

    def setUp(self):
        super(ChatterBotCorpusTrainingTestCase, self).setUp()
        self.chatbot = ChatBot(**settings.CHATTERBOT)
        self.chatbot.set_trainer(
            ChatterBotCorpusTrainer,
            **settings.CHATTERBOT
        )

    def tearDown(self):
        super(ChatterBotCorpusTrainingTestCase, self).setUp()
        self.chatbot.storage.drop()

    def test_train_with_english_greeting_corpus(self):
        self.chatbot.train('chatterbot.corpus.english.greetings')

        statement = self.chatbot.storage.find('Hello')

        self.assertIsNotNone(statement)

    def test_train_with_english_greeting_corpus_tags(self):
        self.chatbot.train('chatterbot.corpus.english.greetings')

        statement = self.chatbot.storage.find('Hello')

        self.assertEqual(['greetings'], statement.get_tags())

    def test_train_with_multiple_corpora(self):
        self.chatbot.train(
            'chatterbot.corpus.english.greetings',
            'chatterbot.corpus.english.conversations',
        )

        statement = self.chatbot.storage.find('Hello')
        self.assertIsNotNone(statement)

    def test_train_with_english_corpus(self):
        self.chatbot.train('chatterbot.corpus.english')
        statement = self.chatbot.storage.find('Hello')

        self.assertIsNotNone(statement)
