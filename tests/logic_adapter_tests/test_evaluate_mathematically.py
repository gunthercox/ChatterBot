from unittest import TestCase
from chatterbot.adapters.logic import EvaluateMathematically
from chatterbot.conversation import Statement


class EvaluateMathematicallyTests(TestCase):

    def setUp(self):
        self.adapter = EvaluateMathematically()

    def test_can_process(self):
        statement = Statement("What is 10 + 10 + 10?")
        self.assertTrue(self.adapter.can_process(statement))

    def test_can_not_process(self):
        statement = Statement("What is your favorite song?")
        self.assertFalse(self.adapter.can_process(statement))

    def test_is_integer(self):
        self.assertTrue(self.adapter.is_integer(42))

    def test_is_float(self):
        self.assertTrue(self.adapter.is_float(0.5))

    def test_is_operator(self):
        self.assertTrue(self.adapter.is_operator('+'))

    def test_is_not_operator(self):
        self.assertFalse(self.adapter.is_operator('9'))

    def test_normalize_empty_string(self):
        """
        If a string is empty, the string should be returned.
        """
        self.assertEqual(self.adapter.normalize(""), "")

    def test_normalize_text_to_lowercase(self):
        normalized = self.adapter.normalize("HELLO")
        self.assertTrue(normalized.islower())

    def test_normalize_punctuation(self):
        normalized = self.adapter.normalize("the end.")
        self.assertEqual(normalized, "the end")

    def test_load_data(self):
        self.adapter.load_data("english")
        self.assertIn("numbers", self.adapter.data)


class MathematicalEvaluationTests(TestCase):

    def setUp(self):
        import sys

        self.adapter = EvaluateMathematically()

        # Some tests may return decimals under python 3
        self.python_version = sys.version_info[0]

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

        if self.python_version <= 2:
            self.assertEqual(response.text, "( 100 / 20 ) = 5")
        else:
            self.assertEqual(response.text, "( 100 / 20 ) = 5.0")

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

        if self.python_version <= 2:
            self.assertEqual(response.text, "( 100 / 100 ) = 1")
        else:
            self.assertEqual(response.text, "( 100 / 100 ) = 1.0")

    def test_large_word_division_operator(self):
        statement = Statement("What is one thousand two hundred four divided by one hundred?")
        confidence, response = self.adapter.process(statement)

        if self.python_version <= 2:
            self.assertEqual(response.text, "( 1000 + 200 + 4 ) / ( 100 ) = 12")
        else:
            self.assertEqual(response.text, "( 1000 + 200 + 4 ) / ( 100 ) = 12.04")

    def test_negative_multiplication(self):
        statement = Statement("What is -105 * 5")
        confidence, response = self.adapter.process(statement)
        self.assertEqual(response.text, "( -105 * 5 ) = -525")

    def test_negative_decimal_multiplication(self):
        statement = Statement("What is -100.5 * 20?")
        confidence, response = self.adapter.process(statement)
        self.assertEqual(response.text, "( -100.5 * 20 ) = -2010.0")
