from tests.base_case import ChatBotTestCase
from unittest import TestCase
from chatterbot import utils


class UtilityTests(TestCase):

    def test_import_module(self):
        datetime = utils.import_module('datetime.datetime')
        self.assertTrue(hasattr(datetime, 'now'))


class UtilityChatBotTestCase(ChatBotTestCase):

    def test_get_response_time(self):
        """
        Test that a response time is returned.
        """

        response_time = utils.get_response_time(self.chatbot)

        self.assertGreater(response_time, 0)
