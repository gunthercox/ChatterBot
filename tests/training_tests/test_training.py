from tests.base_case import ChatBotTestCase
from chatterbot.trainers import ListTrainer


class TrainingTests(ChatBotTestCase):

    def test_trainer_not_set(self):
        with self.assertRaises(ListTrainer.TrainerInitializationException):
            self.chatbot.train()
