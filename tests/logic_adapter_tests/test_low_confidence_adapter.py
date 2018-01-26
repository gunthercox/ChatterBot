from mock import MagicMock
from chatterbot.logic import LowConfidenceAdapter
from chatterbot.conversation import Statement, Response
from tests.base_case import ChatBotTestCase


class LowConfidenceAdapterTestCase(ChatBotTestCase):
    """
    Test cases for the LowConfidenceAdapter.
    """

    def setUp(self):
        super(LowConfidenceAdapterTestCase, self).setUp()
        self.adapter = LowConfidenceAdapter()

        # Add a mock storage adapter to the logic adapter
        self.adapter.set_chatbot(self.chatbot)

        possible_choices = [
            Statement('Who do you love?', in_response_to=[
                Response('I hear you are going on a quest?')
            ]),
            Statement('What is the meaning of life?', in_response_to=[
                Response('Yuck, black licorice jelly beans.')
            ]),
            Statement('I am Iron Man.', in_response_to=[
                Response('What... is your quest?')
            ]),
            Statement('What... is your quest?', in_response_to=[
                Response('I am Iron Man.')
            ]),
            Statement('Yuck, black licorice jelly beans.', in_response_to=[
                Response('What is the meaning of life?')
            ]),
            Statement('I hear you are going on a quest?', in_response_to=[
                Response('Who do you love?')
            ]),
        ]
        self.adapter.chatbot.storage.filter = MagicMock(return_value=possible_choices)

    def test_high_confidence(self):
        """
        Test the case that a high confidence response is known.
        """
        statement = Statement('What is your quest?')
        match = self.adapter.process(statement)

        self.assertEqual(match.confidence, 0)
        self.assertEqual(match, self.adapter.default_responses[0])

    def test_low_confidence(self):
        """
        Test the case that a high confidence response is not known.
        """
        statement = Statement('Is this a tomato?')
        match = self.adapter.process(statement)

        self.assertEqual(match.confidence, 1)
        self.assertEqual(match, self.adapter.default_responses[0])

    def test_low_confidence_options_list(self):
        """
        Test the case that a high confidence response is not known.
        """
        self.adapter.default_responses = [
            Statement(text='No')
        ]

        statement = Statement('Is this a tomato?')
        match = self.adapter.process(statement)

        self.assertEqual(match.confidence, 1)
        self.assertEqual(match, 'No')
