from unittest import TestCase
from unittest.mock import patch

from mathparse import mathparse
from chatterbot import ChatBot
from chatterbot.conversation import Statement
from chatterbot.tagging import NoOpTagger


class CalculationCacheTests(TestCase):

    def setUp(self):
        self.chatbot = ChatBot(
            'Cache Bot',
            database_uri=None,
            initialize=False,
            read_only=True,
            tagger=NoOpTagger,
            logic_adapters=[
                'chatterbot.logic.MathematicalEvaluation',
                'chatterbot.logic.UnitConversion',
                'chatterbot.logic.BestMatch',
            ],
        )
        self.addCleanup(self.chatbot.storage.close)
        self.addCleanup(self.chatbot.storage.drop)

    def test_unhandled_chat_inputs_do_not_accumulate(self):
        for index in range(20):
            text = 'Hello friend' + '!' * index
            self.assertEqual(self.chatbot.get_response(text).text, text)

        for adapter in self.chatbot.logic_adapters[:2]:
            with self.subTest(adapter=adapter.class_name):
                self.assertLessEqual(len(adapter.cache), 1)

    def test_pending_result_is_replaced_by_the_next_input(self):
        cases = (
            (self.chatbot.logic_adapters[0], '2 plus 2', '3 plus 3', '3 plus 3 = 6'),
            (self.chatbot.logic_adapters[1], '1 meter to centimeter', '2 meters to centimeters', '200.0'),
        )
        for adapter, first, second, expected in cases:
            with self.subTest(adapter=adapter.class_name):
                self.assertTrue(adapter.can_process(Statement(first)))
                self.assertTrue(adapter.can_process(Statement(second)))
                self.assertEqual(len(adapter.cache), 1)
                self.assertEqual(adapter.process(Statement(second)).text, expected)

    def test_process_reuses_the_calculation_from_can_process(self):
        cases = (
            (self.chatbot.logic_adapters[0], '2 plus 2', '2 plus 2 = 4'),
            (self.chatbot.logic_adapters[1], '1 meter to centimeter', '100.0'),
        )
        for adapter, text, expected in cases:
            with self.subTest(adapter=adapter.class_name):
                statement = Statement(text)
                with patch.object(mathparse, 'parse', wraps=mathparse.parse) as parse:
                    self.assertTrue(adapter.can_process(statement))
                    response = adapter.process(statement)
                    parse.assert_called_once()
                self.assertEqual(response.text, expected)
                self.assertEqual(response.confidence, 1)
                self.assertFalse(adapter.cache)
