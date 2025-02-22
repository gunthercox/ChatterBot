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

    def test_no_data(self):
        """
        If there is no data to return, an exception should be raised.
        """
        statement = self._add_search_text(text='What is your quest?')
        response = self.adapter.process(statement)

        self.assertEqual(response.text, 'What is your quest?')
        self.assertEqual(response.confidence, 0)

    def test_no_choices(self):
        """
        The input should be returned as the closest match if there
        are no other results to return.
        """
        self._create_with_search_text(text='Random')

        statement = self._add_search_text(text='What is your quest?')
        response = self.adapter.process(statement)

        self.assertEqual(response.text, 'Random')
        self.assertEqual(response.confidence, 0)

    def test_no_known_responses(self):
        """
        A match can be selected which has no known responses.
        In this case a random response will be returned, but the confidence
        should be zero because it is a random choice.
        """
        from unittest.mock import MagicMock

        self.chatbot.storage.update = MagicMock()
        self.chatbot.storage.count = MagicMock(return_value=1)
        self.chatbot.storage.get_random = MagicMock(
            return_value=Statement(text='Random')
        )

        match = self.adapter.process(self._add_search_text(text='Blah'))

        self.assertEqual(match.confidence, 0)
        self.assertEqual(match.text, 'Random')

    def test_match_with_no_response(self):
        """
        A response to the input should be returned if a response is known.
        """
        self._create_with_search_text(
            text='To eat pasta.',
            in_response_to='What is your quest?'
        )

        statement = self._add_search_text(text='What is your quest?')
        response = self.adapter.process(statement)

        self.assertEqual(response.text, 'To eat pasta.')
        self.assertEqual(response.confidence, 1)

    def test_match_with_response(self):
        """
        The response to the input should be returned if a response is known.
        """
        self._create_with_search_text(
            text='To eat pasta.',
            in_response_to='What is your quest?'
        )
        self._create_with_search_text(
            text='What is your quest?'
        )

        statement = self._add_search_text(text='What is your quest?')
        response = self.adapter.process(statement)

        self.assertEqual(response.text, 'To eat pasta.')
        self.assertEqual(response.confidence, 1)

    def test_excluded_words(self):
        """
        Test that the logic adapter cannot return a response containing
        any of the listed words for exclusion.
        """
        self._create_with_search_text(
            text='I like to count.'
        )
        self._create_with_search_text(
            text='Counting is dumb.',
            in_response_to='I like to count.'
        )
        self._create_with_search_text(
            text='Counting is fun!',
            in_response_to='I like to count.'
        )

        self.adapter.excluded_words = ['dumb']

        input_statement = self._add_search_text(text='I like to count.')
        response = self.adapter.process(input_statement)

        self.assertEqual(response.confidence, 1)
        self.assertEqual(response.text, 'Counting is fun!')

    def test_low_confidence(self):
        """
        Test the case that a high confidence response is not known.
        """
        statement = self._add_search_text(text='Is this a tomato?')
        match = self.adapter.process(statement)

        self.assertEqual(match.confidence, 0)
        self.assertEqual(match.text, statement.text)

    def test_low_confidence_options_list(self):
        """
        Test the case that a high confidence response is not known.
        """
        self.adapter.default_responses = [
            Statement(text='No')
        ]

        statement = self._add_search_text(text='Is this a tomato?')
        match = self.adapter.process(statement)

        self.assertEqual(match.confidence, 0)
        self.assertEqual(match.text, 'No')

    def test_text_search_algorithm(self):
        """
        Test that a close match is found when the text_search algorithm is used.
        """
        self.adapter = BestMatch(
            self.chatbot,
            search_algorithm_name='text_search'
        )

        self._create_with_search_text(
            text='I am hungry.'
        )
        self._create_with_search_text(
            text='Okay, what would you like to eat?',
            in_response_to='I am hungry.'
        )
        self._create_with_search_text(
            text='Can you help me?'
        )
        self._create_with_search_text(
            text='Sure, what seems to be the problem?',
            in_response_to='Can you help me?'
        )

        statement = Statement(text='Could you help me?')
        match = self.adapter.process(statement)

        self.assertEqual(match.confidence, 0.82)
        self.assertEqual(match.text, 'Sure, what seems to be the problem?')
