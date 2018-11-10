from tests.base_case import ChatBotTestCase
from chatterbot.logic import SpecificResponseAdapter
from chatterbot.conversation import Statement


class SpecificResponseAdapterTestCase(ChatBotTestCase):
    """
    Test cases for the SpecificResponseAdapter
    """

    def setUp(self):
        super().setUp()
        self.adapter = SpecificResponseAdapter(
            self.chatbot,
            input_text='Open sesame!',
            output_text='Your sesame seed hamburger roll is now open.'
        )

    def test_exact_match(self):
        """
        Test the case that an exact match is given.
        """
        statement = Statement(text='Open sesame!')
        match = self.adapter.process(statement)

        self.assertEqual(match.confidence, 1)
        self.assertEqual(match, self.adapter.response_statement)

    def test_not_exact_match(self):
        """
        Test the case that an exact match is not given.
        """
        statement = Statement(text='Open says me!')
        match = self.adapter.process(statement)

        self.assertEqual(match.confidence, 0)
        self.assertEqual(match, self.adapter.response_statement)
