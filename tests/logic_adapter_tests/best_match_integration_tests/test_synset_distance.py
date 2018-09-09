from unittest.mock import MagicMock
from chatterbot.logic import BestMatch
from chatterbot.conversation import Statement
from tests.base_case import ChatBotTestCase


class BestMatchSynsetDistanceTestCase(ChatBotTestCase):
    """
    Integration tests for the BestMatch logic adapter
    using the synset_distance comparison function.
    """

    def setUp(self):
        super(BestMatchSynsetDistanceTestCase, self).setUp()
        from chatterbot.comparisons import synset_distance

        self.adapter = BestMatch(
            statement_comparison_function=synset_distance
        )

        self.adapter.initialize()

        # Add a mock storage adapter to the logic adapter
        self.adapter.set_chatbot(self.chatbot)

    def test_get_closest_statement(self):
        """
        Note, the content of the in_response_to field for each of the
        test statements is only required because the logic adapter will
        filter out any statements that are not in response to a known statement.
        """
        possible_choices = [
            Statement('This is a lovely bog.', in_response_to='This is a lovely bog.'),
            Statement('This is a beautiful swamp.', in_response_to='This is a beautiful swamp.'),
            Statement('It smells like a swamp.', in_response_to='It smells like a swamp.')
        ]
        self.adapter.chatbot.storage.filter = MagicMock(
            return_value=possible_choices
        )

        statement = Statement('This is a lovely swamp.')
        match = self.adapter.get(statement)

        self.assertEqual('This is a lovely bog.', match)

    def test_different_punctuation(self):
        possible_choices = [
            Statement('Who are you?'),
            Statement('Are you good?'),
            Statement('You are good')
        ]
        self.adapter.chatbot.storage.get_response_statements = MagicMock(
            return_value=possible_choices
        )

        statement = Statement('Are you good')
        match = self.adapter.get(statement)

        self.assertEqual('Are you good?', match)

    def test_no_known_responses(self):
        """
        In the case that a match is selected which has no known responses.
        In this case a random response will be returned, but the confidence
        should be zero because it is a random choice.
        """
        self.adapter.chatbot.storage.update = MagicMock()
        self.adapter.chatbot.storage.count = MagicMock(return_value=1)
        self.adapter.chatbot.storage.get_random = MagicMock(
            return_value=Statement('Random')
        )

        match = self.adapter.process(Statement('Blah'))

        self.assertEqual(match.confidence, 0)
        self.assertEqual(match.text, 'Random')
