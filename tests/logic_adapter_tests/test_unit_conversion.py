from unittest import TestCase
from chatterbot.logic import UnitConversion
from chatterbot.conversation import Statement


class UnitConversionTests(TestCase):

    def setUp(self):
        self.adapter = UnitConversion()

    def test_can_process(self):
        statement = Statement('How many inches are in two kilometers?')
        self.assertTrue(self.adapter.can_process(statement))

    def test_can_not_process(self):
        statement = Statement('What is love?')
        self.assertFalse(self.adapter.can_process(statement))

    def test_inches_to_kilometers(self):
        statement = Statement('How many inches are in two kilometers?')
        expected_value = 78740.2
        response_statement = self.adapter.process(statement)
        self.assertEqual(response_statement.confidence, 1)
        self.assertIsNotNone(response_statement)
        self.assertLessEqual(float(response_statement.text) - expected_value, 1e-10)
