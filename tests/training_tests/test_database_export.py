from tests.base_case import ChatBotTestCase
from chatterbot.trainers import ListTrainer


class DatabaseExportTests(ChatBotTestCase):

    def setUp(self):
        super(DatabaseExportTests, self).setUp()
        self.chatbot.set_trainer(ListTrainer)

    def test_generate_export_data(self):
        self.chatbot.trainer.train([
            'Hello, how are you?',
            'I am good.'
        ])
        data = self.chatbot.trainer._generate_export_data()

        self.assertEqual(
            [['Hello, how are you?', 'I am good.']], data
        )
