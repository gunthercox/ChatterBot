from unittest.mock import MagicMock
from chatterbot.logic import BestMatch
from chatterbot.conversation import Statement
from tests.base_case import ChatBotTestCase


class BestMatchLevenshteinDistanceTestCase(ChatBotTestCase):
    """
    Integration tests for the BestMatch logic adapter
    using Levenshtein distance as a comparison function.
    """

    def setUp(self):
        super().setUp()
        from chatterbot.comparisons import levenshtein_distance

        self.adapter = BestMatch(
            self.chatbot,
            statement_comparison_function=levenshtein_distance
        )

    def test_get_closest_statement(self):
        """
        Note, the content of the in_response_to field for each of the
        test statements is only required because the logic adapter will
        filter out any statements that are not in response to a known statement.
        """
        self.chatbot.storage.create_many([
            Statement(text='Who do you love?', in_response_to='I hear you are going on a quest?'),
            Statement(text='What is the meaning of life?', in_response_to='Yuck, black licorice jelly beans.'),
            Statement(text='I am Iron Man.', in_response_to='What... is your quest?'),
            Statement(text='What... is your quest?', in_response_to='I am Iron Man.'),
            Statement(text='Yuck, black licorice jelly beans.', in_response_to='What is the meaning of life?'),
            Statement(text='I hear you are going on a quest?', in_response_to='Who do you love?'),
        ])

        statement = Statement(text='What is your quest?')

        match = self.adapter.get(statement)

        self.assertEqual('What... is your quest?', match)

    def test_confidence_exact_match(self):
        self.chatbot.storage.create(text='What is your quest?', in_response_to='What is your quest?')

        statement = Statement(text='What is your quest?')
        match = self.adapter.get(statement)

        self.assertEqual(match.confidence, 1)

    def test_confidence_half_match(self):
        self.chatbot.storage.create(text='xxyy', in_response_to='xxyy')

        statement = Statement(text='wwxx')
        match = self.adapter.get(statement)

        self.assertEqual(match.confidence, 0.5)

    def test_confidence_no_match(self):
        self.chatbot.storage.create(text='xxx', in_response_to='xxx')

        statement = Statement(text='yyy')
        match = self.adapter.get(statement)

        self.assertEqual(match.confidence, 0)

    def test_no_known_responses(self):
        """
        In the case that a match is selected which has no known responses.
        In this case a random response will be returned, but the confidence
        should be zero because it is a random choice.
        """
        self.adapter.chatbot.storage.update = MagicMock()
        self.adapter.chatbot.storage.count = MagicMock(return_value=1)
        self.adapter.chatbot.storage.get_random = MagicMock(
            return_value=Statement(text='Random')
        )

        match = self.adapter.process(Statement(text='Blah'))

        self.assertEqual(match.confidence, 0)
        self.assertEqual(match.text, 'Random')
