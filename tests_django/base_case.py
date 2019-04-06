from chatterbot import ChatBot
from django.test import TransactionTestCase
from tests_django import test_settings


class ChatterBotTestCase(TransactionTestCase):

    def setUp(self):
        super().setUp()
        self.chatbot = ChatBot(**test_settings.CHATTERBOT)
