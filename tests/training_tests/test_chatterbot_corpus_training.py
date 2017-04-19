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
        from chatterbot_corpus import corpus
        self.chatbot.set_trainer(ChatterBotCorpusTrainer)

        corpus_data_directory = os.path.dirname(corpus.__file__)
        self.corpus_directory = os.path.join(corpus_data_directory, 'data')

    def test_train_with_english_greeting_corpus(self):
        file_path = os.path.join(self.corpus_directory, 'english', 'greetings.corpus.json')
        self.chatbot.train(file_path)
        statement = self.chatbot.storage.find('Hello')

        self.assertIsNotNone(statement)

    def test_train_with_multiple_corpora(self):
        self.chatbot.train(
            os.path.join(self.corpus_directory, 'english', 'greetings.corpus.json'),
            os.path.join(self.corpus_directory, 'english', 'conversations.corpus.json')
        )
        statement = self.chatbot.storage.find('Hello')

        self.assertIsNotNone(statement)

    def test_train_with_english_corpus(self):
        file_path = os.path.join(self.corpus_directory, 'english')
        self.chatbot.train(file_path)
        statement = self.chatbot.storage.find('Hello')

        self.assertIsNotNone(statement)

    def test_train_with_english_corpus_training_slash(self):
        file_path = os.path.join(self.corpus_directory, 'english') + '/'
        self.chatbot.train(file_path)
        statement = self.chatbot.storage.find('Hello')

        self.assertIsNotNone(statement)