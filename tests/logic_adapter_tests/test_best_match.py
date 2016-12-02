from unittest import TestCase
from mock import MagicMock
from chatterbot.logic import BestMatch
from chatterbot.conversation import Statement, Response
from tests.base_case import MockChatBot


class BestMatchTestCase(TestCase):
    """
    Unit tests for the BestMatch logic adapter.
    """

    def setUp(self):
        from chatterbot.conversation.comparisons import levenshtein_distance

        self.adapter = BestMatch()

        # Add a mock chatbot to the logic adapter
        self.adapter.set_chatbot(MockChatBot())

    def test_no_choices(self):
        """
        An exception should be raised if there is no data in the database.
        """
        self.adapter.chatbot.storage.filter = MagicMock(return_value=[])
        statement = Statement('What is your quest?')

        with self.assertRaises(BestMatch.EmptyDatasetException):
            self.adapter.get(statement)
