from tests.base_case import ChatBotTestCase
from chatterbot.logic import SpecificResponseAdapter
from chatterbot.conversation import Statement
from spacy.matcher import Matcher


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

    def test_initialization_with_missing_input_text(self):
        """"
        Test that an exception is raised if input_text is missing.
        """
        with self.assertRaises(self.chatbot.ChatBotException):
            SpecificResponseAdapter(
                self.chatbot,
                output_text='Done!'
            )

    def test_initialization_with_missing_output_text(self):
        """"
        Test that an exception is raised if output_text is missing.
        """
        with self.assertRaises(self.chatbot.ChatBotException):
            SpecificResponseAdapter(
                self.chatbot,
                input_text='Do something!'
            )

    def test_exact_match(self):
        """
        Test the case that an exact match is given.
        """
        statement = Statement(text='Open sesame!')
        match = self.adapter.process(statement)

        self.assertEqual(match.confidence, 1)
        self.assertEqual(match.text, 'Your sesame seed hamburger roll is now open.')

    def test_not_exact_match(self):
        """
        Test the case that an exact match is not given.
        """
        statement = Statement(text='Open says me!')
        match = self.adapter.process(statement)

        self.assertEqual(match.confidence, 0)
        self.assertEqual(match.text, 'Your sesame seed hamburger roll is now open.')


class SpecificResponseAdapterSpacyTestCase(ChatBotTestCase):
    """
    Tests specific response adapter with spacy.
    """

    def setUp(self):
        super().setUp()

        pattern = [
            {
                'LOWER': 'open'
            },
            {
                'LOWER': 'sesame'
            }
        ]

        self.adapter = SpecificResponseAdapter(
            self.chatbot,
            input_text=pattern,
            matcher=Matcher,
            output_text='Your sesame seed hamburger roll is now open.',
            use_patterns=False
        )

    def test_pattern_match(self):
        """
        Test the case that a pattern match is given.
        """
        statement = Statement(text='Open sesame!')
        match = self.adapter.process(statement)

        self.assertEqual(match.confidence, 1)
        self.assertEqual(match.text, 'Your sesame seed hamburger roll is now open.')


class SpecificResponseAdapterFunctionResponseTestCase(ChatBotTestCase):
    """
    Tests specific response adapter using a function that returns a response.
    """

    def setUp(self):
        super().setUp()

        def response_function():
            return 'Your sesame seed hamburger roll is now open.'

        self.adapter = SpecificResponseAdapter(
            self.chatbot,
            input_text='Open sesame!',
            output_text=response_function
        )

    def test_function_response(self):
        """
        Test the case that a function is given as the output_text.
        """
        statement = Statement(text='Open sesame!')
        match = self.adapter.process(statement)

        self.assertEqual(match.confidence, 1)
        self.assertEqual(match.text, 'Your sesame seed hamburger roll is now open.')
