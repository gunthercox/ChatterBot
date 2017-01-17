from unittest import TestCase
from chatterbot.logic import SpecificResponseAdapter
from chatterbot.conversation import Statement


class SpecificResponseAdapterTestCase(TestCase):
    """
    Test cases for the SpecificResponseAdapter
    """

    def setUp(self):
        super(SpecificResponseAdapterTestCase, self).setUp()
        self.adapter = SpecificResponseAdapter(
            input_text='Open sesame!',
            output_text='Your sesame seed hamburger roll is now open.'
        )

    def test_exact_match(self):
        """
        Test the case that an exact match is given.
        """
        statement = Statement('Open sesame!')
        match = self.adapter.process(statement)

        self.assertEqual(match.confidence, 1)
        self.assertEqual(match, self.adapter.response_statement)

    def test_not_exact_match(self):
        """
        Test the case that an exact match is not given.
        """
        statement = Statement('Open says me!')
        match = self.adapter.process(statement)

        self.assertEqual(match.confidence, 0)
        self.assertEqual(match, self.adapter.response_statement)
