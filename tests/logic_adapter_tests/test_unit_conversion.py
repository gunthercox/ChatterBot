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

    def test_can_not_convert_inches_to_kilometer(self):
        statement = Statement('How many inches are in blue kilometer?')
        self.assertFalse(self.adapter.can_process(statement))

    def test_inches_to_kilometers(self):
        statement = Statement('How many inches are in two kilometers?')
        self.assertTrue(self.adapter.can_process(statement))
        expected_value = 78740.2
        response_statement = self.adapter.process(statement)
        self.assertIsNotNone(response_statement)
        self.assertLessEqual(abs(response_statement.confidence - 1.0), 1e-10)
        self.assertLessEqual(abs(float(response_statement.text) - expected_value), 0.1)

    def test_inches_to_kilometers_variation_1(self):
        statement = Statement('How many inches in two kilometers?')
        self.assertTrue(self.adapter.can_process(statement))
        expected_value = 78740.2
        response_statement = self.adapter.process(statement)
        self.assertIsNotNone(response_statement)
        self.assertLessEqual(abs(response_statement.confidence - 1.0), 1e-10)
        self.assertLessEqual(abs(float(response_statement.text) - expected_value), 0.1)

    def test_inches_to_kilometers_variation_2(self):
        statement = Statement('how many  inches  in two  kilometers ?')
        self.assertTrue(self.adapter.can_process(statement))
        expected_value = 78740.2
        response_statement = self.adapter.process(statement)
        self.assertIsNotNone(response_statement)
        self.assertLessEqual(abs(response_statement.confidence - 1.0), 1e-10)
        self.assertLessEqual(abs(float(response_statement.text) - expected_value), 0.1)

    def test_inches_to_kilometers_variation_3(self):
        statement = Statement('how many  inches  in 2  kilometers  ?')
        self.assertTrue(self.adapter.can_process(statement))
        expected_value = 78740.2
        response_statement = self.adapter.process(statement)
        self.assertIsNotNone(response_statement)
        self.assertLessEqual(abs(response_statement.confidence - 1.0), 1e-10)
        self.assertLessEqual(abs(float(response_statement.text) - expected_value), 0.1)

    def test_meter_to_kilometer(self):
        statement = Statement('How many meters are in one kilometer?')
        self.assertTrue(self.adapter.can_process(statement))
        expected_value = 1000
        response_statement = self.adapter.process(statement)
        self.assertIsNotNone(response_statement)
        self.assertLessEqual(abs(response_statement.confidence - 1.0), 0.1)
        self.assertLessEqual(abs(float(response_statement.text) - expected_value), 0.1)

    def test_meter_to_kilometer_variation(self):
        statement = Statement('How many meters are in a kilometer?')
        self.assertTrue(self.adapter.can_process(statement))
        expected_value = 1000
        response_statement = self.adapter.process(statement)
        self.assertIsNotNone(response_statement)
        self.assertLessEqual(abs(response_statement.confidence - 1.0), 0.1)
        self.assertLessEqual(abs(float(response_statement.text) - expected_value), 0.1)
