from unittest import TestCase

from chatterbot import ChatBot
from chatterbot.conversation import Statement
from chatterbot.tagging import NoOpTagger


class MathematicalEvaluationErrorTests(TestCase):

    def setUp(self):
        self.chatbot = ChatBot(
            'Math fallback bot',
            database_uri=None,
            initialize=False,
            read_only=True,
            tagger=NoOpTagger,
            logic_adapters=[
                'chatterbot.logic.MathematicalEvaluation',
                {
                    'import_path': 'chatterbot.logic.BestMatch',
                    'default_response': 'I could not calculate that.',
                },
            ],
        )
        self.addCleanup(self.chatbot.storage.close)
        self.addCleanup(self.chatbot.storage.drop)
        self.adapter = self.chatbot.logic_adapters[0]

    def test_invalid_arithmetic_has_zero_confidence(self):
        for expression in ('sqrt -1', 'log 0', '0 ^ -1'):
            with self.subTest(expression=expression):
                response = self.adapter.process(Statement(text=expression))
                self.assertEqual(response.confidence, 0)

    def test_invalid_arithmetic_allows_a_fallback_response(self):
        for expression in ('sqrt -1', 'log 0', '0 ^ -1'):
            with self.subTest(expression=expression):
                response = self.chatbot.get_response(expression)
                self.assertEqual(response.text, 'I could not calculate that.')

    def test_division_by_zero_keeps_the_undefined_result(self):
        response = self.adapter.process(Statement(text='1 / 0'))

        self.assertEqual(response.text, '1 / 0 = undefined')
        self.assertEqual(response.confidence, 1)
