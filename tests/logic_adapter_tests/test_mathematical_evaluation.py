from unittest import TestCase
from chatterbot.logic import MathematicalEvaluation
from chatterbot.conversation import Statement


class MathematicalEvaluationTests(TestCase):

    def setUp(self):
        self.adapter = MathematicalEvaluation()

    def test_can_process(self):
        statement = Statement('What is 10 + 10 + 10?')
        self.assertTrue(self.adapter.can_process(statement))

    def test_can_not_process(self):
        statement = Statement('What is your favorite song?')
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
        self.assertEqual(self.adapter.normalize(''), '')

    def test_normalize_text_to_lowercase(self):
        normalized = self.adapter.normalize('HELLO')
        self.assertTrue(normalized.islower())

    def test_normalize_punctuation(self):
        normalized = self.adapter.normalize('the end.')
        self.assertEqual(normalized, 'the end')

    def test_load_english_data(self):
        self.adapter.get_language_data('english')
        self.assertIn('numbers', self.adapter.math_words)

    def test_load_nonexistent_data(self):
        with self.assertRaises(MathematicalEvaluation.UnrecognizedLanguageException):
            self.adapter.get_language_data('0101010')


class MathematicalEvaluationOperationTests(TestCase):

    def setUp(self):
        import sys

        self.adapter = MathematicalEvaluation()

        # Some tests may return decimals under python 3
        self.python_version = sys.version_info[0]

    def test_addition_operator(self):
        statement = Statement('What is 100 + 54?')
        response = self.adapter.process(statement)
        self.assertEqual(response.text, '( 100 + 54 ) = 154')
        self.assertEqual(response.confidence, 1)

    def test_subtraction_operator(self):
        statement = Statement('What is 100 - 58?')
        response = self.adapter.process(statement)
        self.assertEqual(response.text, '( 100 - 58 ) = 42')
        self.assertEqual(response.confidence, 1)

    def test_multiplication_operator(self):
        statement = Statement('What is 100 * 20')
        response = self.adapter.process(statement)
        self.assertEqual(response.text, '( 100 * 20 ) = 2000')
        self.assertEqual(response.confidence, 1)

    def test_division_operator(self):
        statement = Statement('What is 100 / 20')
        response = self.adapter.process(statement)
        self.assertEqual(response.confidence, 1)

        if self.python_version <= 2:
            self.assertEqual(response.text, '( 100 / 20 ) = 5')
        else:
            self.assertEqual(response.text, '( 100 / 20 ) = 5.0')

    def test_exponent_operator(self):
        statement = Statement('What is 2 ^ 10')
        response = self.adapter.process(statement)
        self.assertEqual(response.text, '( 2 ^ 10 ) = 1024')
        self.assertEqual(response.confidence, 1)

    def test_parenthesized_multiplication_and_addition(self):
        statement = Statement('What is 100 + ( 1000 * 2 )?')
        response = self.adapter.process(statement)
        self.assertEqual(response.text, '( 100 + ( ( 1000 * ( 2 ) ) ) ) = 2100')
        self.assertEqual(response.confidence, 1)

    def test_parenthesized_with_words(self):
        statement = Statement('What is four plus 100 + ( 100 * 2 )?')
        response = self.adapter.process(statement)
        self.assertEqual(response.text, '( 4 + ( 100 + ( ( 100 * ( 2 ) ) ) ) ) = 304')
        self.assertEqual(response.confidence, 1)

    def test_word_numbers_addition(self):
        statement = Statement('What is one hundred + four hundred?')
        response = self.adapter.process(statement)
        self.assertEqual(response.text, '( 100 + 400 ) = 500')
        self.assertEqual(response.confidence, 1)

    def test_word_division_operator(self):
        statement = Statement('What is 100 divided by 100?')
        response = self.adapter.process(statement)

        if self.python_version <= 2:
            self.assertEqual(response.text, '( 100 / 100 ) = 1')
        else:
            self.assertEqual(response.text, '( 100 / 100 ) = 1.0')

        self.assertEqual(response.confidence, 1)

    def test_large_word_division_operator(self):
        statement = Statement('What is one thousand two hundred four divided by one hundred?')
        response = self.adapter.process(statement)

        if self.python_version <= 2:
            self.assertEqual(response.text, '( 1000 + 200 + 4 ) / ( 100 ) = 12')
        else:
            self.assertEqual(response.text, '( 1000 + 200 + 4 ) / ( 100 ) = 12.04')

        self.assertEqual(response.confidence, 1)

    def test_negative_multiplication(self):
        statement = Statement('What is -105 * 5')
        response = self.adapter.process(statement)
        self.assertEqual(response.text, '( -105 * 5 ) = -525')
        self.assertEqual(response.confidence, 1)

    def test_negative_decimal_multiplication(self):
        statement = Statement('What is -100.5 * 20?')
        response = self.adapter.process(statement)
        self.assertEqual(response.text, '( -100.5 * 20 ) = -2010.0')
        self.assertEqual(response.confidence, 1)

    def test_pi_constant(self):
        statement = Statement('What is pi plus one ?')
        response = self.adapter.process(statement)
        self.assertEqual(response.text, '3.141693 + ( 1 ) = 4.141693')
        self.assertEqual(response.confidence, 1)

    def test_e_constant(self):
        statement = Statement('What is e plus one ?')
        response = self.adapter.process(statement)
        self.assertEqual(response.text, '2.718281 + ( 1 ) = 3.718281')
        self.assertEqual(response.confidence, 1)

    def test_log_function(self):
        statement = Statement('What is log 100 ?')
        response = self.adapter.process(statement)
        self.assertEqual(response.text, 'log ( 100 ) = 2.0')
        self.assertEqual(response.confidence, 1)

    def test_square_root_function(self):
        statement = Statement('What is the sqrt 144 ?')
        response = self.adapter.process(statement)
        self.assertEqual(response.text, 'sqrt ( 144 ) = 12.0')
        self.assertEqual(response.confidence, 1)

