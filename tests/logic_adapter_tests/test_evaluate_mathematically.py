from unittest import TestCase
from chatterbot.adapters.logic import EvaluateMathematically
from chatterbot.conversation import Statement


class MathematicalEvaluationTests(TestCase):

    def setUp(self):
        self.adapter = EvaluateMathematically()

    def test_addition_operator(self):
        statement = Statement("What is 100 + 54?")
        confidence, response = self.adapter.process(statement)
        self.assertEqual(response.text, "( 100 + 54 ) = 154")

    def test_subtraction_operator(self):
        statement = Statement("What is 100 - 58?")
        confidence, response = self.adapter.process(statement)
        self.assertEqual(response.text, "( 100 - 58 ) = 42")

    def test_multiplication_operator(self):
        statement = Statement("What is 100 * 20")
        confidence, response = self.adapter.process(statement)
        self.assertEqual(response.text, "( 100 * 20 ) = 2000")

    def test_division_operator(self):
        statement = Statement("What is 100 / 20")
        confidence, response = self.adapter.process(statement)
        self.assertEqual(response.text, "( 100 / 20 ) = 5")

    def test_parenthesized_multiplication_and_addition(self):
        statement = Statement("What is 100 + ( 1000 * 2 )?")
        confidence, response = self.adapter.process(statement)
        self.assertEqual(response.text, "( 100 + ( ( 1000 * ( 2 ) ) ) ) = 2100")

    def test_parenthesized_with_words(self):
        statement = Statement("What is four plus 100 + ( 100 * 2 )?")
        confidence, response = self.adapter.process(statement)
        self.assertEqual(response.text, "( 4 + ( 100 + ( ( 100 * ( 2 ) ) ) ) ) = 304")

    def test_word_numbers_addition(self):
        statement = Statement("What is one hundred + four hundred?")
        confidence, response = self.adapter.process(statement)
        self.assertEqual(response.text, "( 100 + 400 ) = 500")

    def test_word_division_operator(self):
        statement = Statement("What is 100 divided by 100?")
        confidence, response = self.adapter.process(statement)
        self.assertEqual(response.text, "( 100 / 100 ) = 1")

    def test_large_word_division_operator(self):
        statement = Statement("What is one thousand two hundred four divided by one hundred?")
        confidence, response = self.adapter.process(statement)
        self.assertEqual(response.text, "( 1000 + 200 + 4 ) / ( 100 ) = 12")

    def test_negative_multiplication(self):
        statement = Statement("What is -105 * 5")
        confidence, response = self.adapter.process(statement)
        self.assertEqual(response.text, "( -105 * 5 ) = -525")

    def test_negative_decimal_multiplication(self):
        statement = Statement("What is -100.5 * 20?")
        confidence, response = self.adapter.process(statement)
        self.assertEqual(response.text, "( -100.5 * 20 ) = -2010.0")
