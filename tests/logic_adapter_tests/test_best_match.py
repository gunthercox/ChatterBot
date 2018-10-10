from unittest.mock import MagicMock
from chatterbot.logic import BestMatch
from chatterbot.conversation import Statement
from tests.base_case import ChatBotTestCase


class BestMatchTestCase(ChatBotTestCase):
    """
    Unit tests for the BestMatch logic adapter.
    """

    def setUp(self):
        super().setUp()
        self.adapter = BestMatch(self.chatbot)

    def test_no_choices(self):
        """
        An exception should be raised if there is no data in the database.
        """
        self.adapter.chatbot.storage.filter = MagicMock(return_value=[])
        self.adapter.chatbot.storage.count = MagicMock(return_value=0)

        statement = Statement(text='What is your quest?')
        response = self.adapter.get(statement)

        self.assertEqual(response.text, 'What is your quest?')
        self.assertEqual(response.confidence, 0)
