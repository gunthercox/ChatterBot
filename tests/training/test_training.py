from tests.base_case import ChatBotTestCase
from chatterbot.trainers import Trainer
from chatterbot.conversation import Statement


class TrainingTests(ChatBotTestCase):

    def setUp(self):
        super().setUp()

        self.trainer = Trainer(self.chatbot)

    def test_trainer_not_set(self):
        with self.assertRaises(Trainer.TrainerInitializationException):
            self.trainer.train()

    def test_generate_export_data(self):
        self.chatbot.storage.create_many([
            Statement(text='Hello, how are you?'),
            Statement(text='I am good.', in_response_to='Hello, how are you?')
        ])
        data = self.trainer._generate_export_data()

        self.assertEqual(
            [['Hello, how are you?', 'I am good.']], data
        )
