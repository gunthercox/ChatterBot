from tests.base_case import ChatBotTestCase
from chatterbot.trainers import ListTrainer


class DatabaseExportTests(ChatBotTestCase):

    def setUp(self):
        super().setUp()
        self.trainer = ListTrainer(
            self.chatbot,
            show_training_progress=False
        )

    def test_generate_export_data(self):
        self.trainer.train([
            'Hello, how are you?',
            'I am good.'
        ])
        data = self.trainer._generate_export_data()

        self.assertEqual(
            [['Hello, how are you?', 'I am good.']], data
        )
