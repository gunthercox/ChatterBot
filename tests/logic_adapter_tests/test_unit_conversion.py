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
        self.assertLessEqual(abs(response_statement.confidence - 1.0), 1e-10)
        self.assertIsNotNone(response_statement)
        self.assertLessEqual(abs(float(response_statement.text) - expected_value), 0.1)

    def test_meter_to_kilometer(self):
        statement = Statement('How many meters are in one kilometer?')
        expected_value = 1000
        response_statement = self.adapter.process(statement)
        self.assertLessEqual(abs(response_statement.confidence - 1.0), 0.1)
        self.assertIsNotNone(response_statement)
        self.assertLessEqual(abs(float(response_statement.text) - expected_value), 0.1)
