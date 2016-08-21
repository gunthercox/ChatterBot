from unittest import TestCase
from mock import MagicMock, Mock
from chatterbot.adapters.logic import ClosestMeaningAdapter
from chatterbot.adapters.storage import StorageAdapter
from chatterbot.conversation import Statement, Response


class MockContext(object):
    def __init__(self):
        self.storage = StorageAdapter()

        self.storage.get_random = Mock(
            side_effect=ClosestMeaningAdapter.EmptyDatasetException()
        )


class ClosestMeaningAdapterTests(TestCase):

    def setUp(self):
        self.adapter = ClosestMeaningAdapter()

        # Add a mock storage adapter to the context
        self.adapter.set_context(MockContext())

    def test_no_choices(self):
        self.adapter.context.storage.filter = MagicMock(return_value=[])
        statement = Statement('Hello')

        with self.assertRaises(ClosestMeaningAdapter.EmptyDatasetException):
            self.adapter.get(statement)

    def test_get_closest_statement(self):
        """
        Note, the content of the in_response_to field for each of the
        test statements is only required because the logic adapter will
        filter out any statements that are not in response to a known statement.
        """
        possible_choices = [
            Statement('This is a lovely bog.', in_response_to=[Response('This is a lovely bog.')]),
            Statement('This is a beautiful swamp.', in_response_to=[Response('This is a beautiful swamp.')]),
            Statement('It smells like swamp.', in_response_to=[Response('It smells like swamp.')])
        ]
        self.adapter.context.storage.filter = MagicMock(
            return_value=possible_choices
        )

        statement = Statement('This is a lovely swamp.')
        confidence, match = self.adapter.get(statement)

        self.assertEqual('This is a lovely bog.', match)

    def test_different_punctuation(self):
        possible_choices = [
            Statement('Who are you?'),
            Statement('Are you good?'),
            Statement('You are good')
        ]
        self.adapter.context.storage.get_response_statements = MagicMock(
            return_value=possible_choices
        )

        statement = Statement('Are you good')
        confidence, match = self.adapter.get(statement)

        self.assertEqual('Are you good?', match)

    def test_no_known_responses(self):
        """
        In the case that a match is selected which has no known responses.
        In this case a random response will be returned, but the confidence
        should be zero because it is a random choice.
        """
        self.adapter.context.storage.update = MagicMock()
        self.adapter.context.storage.filter = MagicMock(
            return_value=[]
        )
        self.adapter.context.storage.get_random = MagicMock(
            return_value=Statement("Random")
        )

        confidence, match = self.adapter.process(Statement("Blah"))

        self.assertEqual(confidence, 0)
        self.assertEqual(match.text, "Random")
