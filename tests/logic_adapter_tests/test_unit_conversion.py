from tests.base_case import ChatBotTestCase
from chatterbot.logic import UnitConversion
from chatterbot.conversation import Statement


class UnitConversionTests(ChatBotTestCase):
    def setUp(self):
        super().setUp()
        self.adapter = UnitConversion(self.chatbot)

    def test_can_process(self):
        statement = Statement(text='How many inches are in two kilometers?')
        self.assertTrue(self.adapter.can_process(statement))

    def test_can_process_pattern_x_unit_to_y_unit(self):
        statement = Statement(text='0 Celsius to fahrenheit')
        self.assertTrue(self.adapter.can_process(statement))

    def test_can_process_x_unit_is_how_many_y_unit(self):
        statement = Statement(text='2 TB is how many GB?')
        self.assertTrue(self.adapter.can_process(statement))

    def test_can_not_process(self):
        statement = Statement(text='What is love?')
        self.assertFalse(self.adapter.can_process(statement))

    def test_can_not_convert_inches_to_kilometer(self):
        statement = Statement(text='How many inches are in blue kilometer?')
        self.assertFalse(self.adapter.can_process(statement))

    def test_inches_to_kilometers(self):
        statement = Statement(text='How many inches are in two kilometers?')
        self.assertTrue(self.adapter.can_process(statement))
        expected_value = 78740.2
        response_statement = self.adapter.process(statement)
        self.assertIsNotNone(response_statement)
        self.assertLessEqual(abs(response_statement.confidence - 1.0), 1e-10)
        self.assertLessEqual(abs(float(response_statement.text) - expected_value), 0.1)

    def test_inches_to_kilometers_variation_1(self):
        statement = Statement(text='How many inches in two kilometers?')
        self.assertTrue(self.adapter.can_process(statement))
        expected_value = 78740.2
        response_statement = self.adapter.process(statement)
        self.assertIsNotNone(response_statement)
        self.assertLessEqual(abs(response_statement.confidence - 1.0), 1e-10)
        self.assertLessEqual(abs(float(response_statement.text) - expected_value), 0.1)

    def test_inches_to_kilometers_variation_2(self):
        statement = Statement(text='how many  inches  in two  kilometers ?')
        self.assertTrue(self.adapter.can_process(statement))
        expected_value = 78740.2
        response_statement = self.adapter.process(statement)
        self.assertIsNotNone(response_statement)
        self.assertLessEqual(abs(response_statement.confidence - 1.0), 1e-10)
        self.assertLessEqual(abs(float(response_statement.text) - expected_value), 0.1)

    def test_inches_to_kilometers_variation_3(self):
        statement = Statement(text='how many  inches  in 2  kilometers  ?')
        self.assertTrue(self.adapter.can_process(statement))
        expected_value = 78740.2
        response_statement = self.adapter.process(statement)
        self.assertIsNotNone(response_statement)
        self.assertLessEqual(abs(response_statement.confidence - 1.0), 1e-10)
        self.assertLessEqual(abs(float(response_statement.text) - expected_value), 0.1)

    def test_meter_to_kilometer(self):
        statement = Statement(text='How many meters are in one kilometer?')
        self.assertTrue(self.adapter.can_process(statement))
        expected_value = 1000
        response_statement = self.adapter.process(statement)
        self.assertIsNotNone(response_statement)
        self.assertLessEqual(abs(response_statement.confidence - 1.0), 0.1)
        self.assertLessEqual(abs(float(response_statement.text) - expected_value), 0.1)

    def test_meter_to_kilometer_variation(self):
        statement = Statement(text='How many meters are in a kilometer?')
        self.assertTrue(self.adapter.can_process(statement))
        expected_value = 1000
        response_statement = self.adapter.process(statement)
        self.assertIsNotNone(response_statement)
        self.assertLessEqual(abs(response_statement.confidence - 1.0), 0.1)
        self.assertLessEqual(abs(float(response_statement.text) - expected_value), 0.1)

    def test_temperature_celsius_to_fahrenheit(self):
        statement = Statement(text='How many fahrenheit are in 0 celsius ?')
        self.assertTrue(self.adapter.can_process(statement))
        expected_value = 32
        response_statement = self.adapter.process(statement)
        self.assertIsNotNone(response_statement)
        self.assertLessEqual(abs(response_statement.confidence - 1.0), 0.1)
        self.assertLessEqual(abs(float(response_statement.text) - expected_value), 0.1)

    def test_negative_temperature_celsius_to_fahrenheit(self):
        statement = Statement(text='How many fahrenheit are in -0.2 celsius ?')
        self.assertTrue(self.adapter.can_process(statement))
        expected_value = 31.64
        response_statement = self.adapter.process(statement)
        self.assertIsNotNone(response_statement)
        self.assertLessEqual(abs(response_statement.confidence - 1.0), 0.1)
        self.assertLessEqual(abs(float(response_statement.text) - expected_value), 0.1)

    def test_time_two_hours_to_seconds(self):
        statement = Statement(text='How many seconds are in two hours?')
        self.assertTrue(self.adapter.can_process(statement))
        expected_value = 7200
        response_statement = self.adapter.process(statement)
        self.assertIsNotNone(response_statement)
        self.assertLessEqual(abs(response_statement.confidence - 1.0), 0.1)
        self.assertLessEqual(abs(float(response_statement.text) - expected_value), 0.1)

    def test_pattern_x_unit_to_y_unit(self):
        statement = Statement(text='-11 Celsius to kelvin')
        self.assertTrue(self.adapter.can_process(statement))
        expected_value = 262.15
        response_statement = self.adapter.process(statement)
        self.assertIsNotNone(response_statement)
        self.assertLessEqual(abs(response_statement.confidence - 1.0), 0.1)
        self.assertLessEqual(abs(float(response_statement.text) - expected_value), 0.1)

    def test_pattern_x_unit_is_how_many_y_unit(self):
        statement = Statement(text='2 TB is how many GB?')
        self.assertTrue(self.adapter.can_process(statement))
        expected_value = 2000
        response_statement = self.adapter.process(statement)
        self.assertIsNotNone(response_statement)
        self.assertLessEqual(abs(response_statement.confidence - 1.0), 0.1)
        self.assertLessEqual(abs(float(response_statement.text) - expected_value), 0.1)
