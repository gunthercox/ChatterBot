import os
from tests.base_case import ChatBotTestCase
from chatterbot.trainers import ChatterBotCorpusTrainer


class ChatterBotCorpusTrainingTestCase(ChatBotTestCase):

    def setUp(self):
        super(ChatterBotCorpusTrainingTestCase, self).setUp()
        self.chatbot.set_trainer(ChatterBotCorpusTrainer)

    def test_train_with_english_greeting_corpus(self):
        self.chatbot.train('chatterbot.corpus.english.greetings')

        statement = self.chatbot.storage.find('Hello')
        self.assertIsNotNone(statement)

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


class ChatterBotCorpusFilePathTestCase(ChatBotTestCase):

    def setUp(self):
        super(ChatterBotCorpusFilePathTestCase, self).setUp()
        self.chatbot.set_trainer(ChatterBotCorpusTrainer)

        current_directory = os.path.dirname(os.path.abspath(__file__))
        base_directory = os.path.abspath(os.path.join(current_directory, os.pardir, os.pardir))
        self.corpus_directory = os.path.join(base_directory, 'chatterbot', 'corpus', 'data')

    def test_train_with_english_greeting_corpus(self):
        file_path = os.path.join(self.corpus_directory, 'english', 'greetings.corpus.json')
        self.chatbot.train(file_path)
        statement = self.chatbot.storage.find('Hello')

        self.assertIsNotNone(statement)

    def test_train_with_multiple_corpora(self):
        self.chatbot.train(
            'chatterbot/corpus/data/english/greetings.corpus.json',
            'chatterbot/corpus/data/english/conversations.corpus.json'
        )
        statement = self.chatbot.storage.find('Hello')

        self.assertIsNotNone(statement)

    def test_train_with_english_corpus(self):
        self.chatbot.train('chatterbot/corpus/data/english')
        statement = self.chatbot.storage.find('Hello')

        self.assertIsNotNone(statement)

    def test_train_with_english_corpus_training_slash(self):
        self.chatbot.train('chatterbot/corpus/data/english/')
        statement = self.chatbot.storage.find('Hello')

        self.assertIsNotNone(statement)
