from tests.base_case import ChatBotTestCase
from chatterbot.trainers import Trainer


class TrainingTests(ChatBotTestCase):

    def setUp(self):
        super().setUp()

        self.trainer = Trainer(self.chatbot)

    def test_trainer_not_set(self):
        with self.assertRaises(Trainer.TrainerInitializationException):
            self.trainer.train()
