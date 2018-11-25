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
        statement = Statement(text='What is your quest?')
        response = self.adapter.get(statement)

        self.assertEqual(response.text, 'What is your quest?')
        self.assertEqual(response.confidence, 0)

    def test_excluded_words(self):
        """
        Test that the logic adapter cannot return a response containing
        any of the listed words for exclusion.
        """
        self.chatbot.storage.create(
            text='I like to count.'
        )
        self.chatbot.storage.create(
            text='Counting is dumb.',
            in_response_to='I like to count.'
        )
        self.chatbot.storage.create(
            text='Counting is fun!',
            in_response_to='I like to count.'
        )

        self.adapter.excluded_words = ['dumb']

        response = self.adapter.process(Statement(text='I like to count.'))

        self.assertEqual(response.confidence, 1)
        self.assertEqual(response.text, 'Counting is fun!')
