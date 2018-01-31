from tests.base_case import ChatBotTestCase
from chatterbot.trainers import ChatterBotCorpusTrainer


class ChatterBotCorpusTrainingTestCase(ChatBotTestCase):
    """
    Test case for training with data from the ChatterBot Corpus.

    Note: This class has a mirror tests_django/integration_tests/
    """

    def setUp(self):
        super(ChatterBotCorpusTrainingTestCase, self).setUp()
        self.chatbot.set_trainer(
            ChatterBotCorpusTrainer,
            show_training_progress=False
        )

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
