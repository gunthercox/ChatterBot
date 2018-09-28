from chatterbot import ChatBot
from django.test import TestCase
from tests_django import test_settings


class ChatterBotTestCase(TestCase):

    def setUp(self):
        super().setUp()
        self.chatbot = ChatBot(**test_settings.CHATTERBOT)
