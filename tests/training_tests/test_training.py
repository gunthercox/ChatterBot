from tests.base_case import ChatBotTestCase
from chatterbot import ChatBot
from chatterbot.training.trainers import ListTrainer


class TrainingTests(ChatBotTestCase):

    def test_trainer_not_set(self):
        with self.assertRaises(ChatBot.TrainerInitializationException):
            self.chatbot.train()
