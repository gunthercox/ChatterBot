from types import SimpleNamespace
from unittest import TestCase

from chatterbot import ChatBot, languages
from tests.base_case import ChatBotTestCase
from chatterbot.logic import MathematicalEvaluation
from chatterbot.conversation import Statement
from chatterbot.tagging import NoOpTagger


class MathematicalEvaluationStopwordTests(TestCase):

    def create_adapter(self, language, math_language=languages.ENG):
        chatbot = ChatBot(
            'Math Bot',
            database_uri=None,
            initialize=False,
            tagger=NoOpTagger(language=language),
            logic_adapters=[{
                'import_path': 'chatterbot.logic.MathematicalEvaluation',
                'language': math_language,
            }],
        )
        self.addCleanup(chatbot.storage.close)
        self.addCleanup(chatbot.storage.drop)
        return chatbot.logic_adapters[0]

    def test_english_stopwords(self):
        adapter = self.create_adapter(languages.ENG)
        response = adapter.process(Statement(text='2 plus the 2'))

        self.assertEqual(response.text, '2 plus the 2 = 4')
        self.assertEqual(response.confidence, 1)
        self.assertEqual(adapter.execute_as_tool(expression='2 plus the 2'), '2 plus the 2 = 4')

    def test_scale_words_are_not_removed(self):
        adapter = self.create_adapter(languages.ENG)
        expression = 'one hundred plus two thousand'
        response = adapter.process(Statement(text=expression))

        self.assertEqual(response.text, 'one hundred plus two thousand = 2100')
        self.assertEqual(response.confidence, 1)
        self.assertEqual(adapter.execute_as_tool(expression=expression), response.text)

    def test_spanish_stopwords(self):
        adapter = self.create_adapter(languages.SPA)
        response = adapter.process(Statement(text='2 plus de 2'))

        self.assertEqual(response.text, '2 plus de 2 = 4')
        self.assertEqual(response.confidence, 1)
        self.assertEqual(adapter.execute_as_tool(expression='2 plus de 2'), '2 plus de 2 = 4')

    def test_german_stopwords_and_math_language(self):
        adapter = self.create_adapter(languages.GER, math_language=languages.GER)
        response = adapter.process(Statement(text='zwei plus die zwei'))

        self.assertEqual(response.text, 'zwei plus die zwei = 4')
        self.assertEqual(response.confidence, 1)
        self.assertEqual(adapter.execute_as_tool(expression='zwei plus die zwei'), response.text)

    def test_no_spacy_stopwords(self):
        adapter = self.create_adapter(SimpleNamespace(ISO_639_1='xx'))
        self.assertEqual(adapter.stop_words, set())

        response = adapter.process(Statement(text='2 plus 2'))
        self.assertEqual(response.text, '2 plus 2 = 4')
        self.assertEqual(response.confidence, 1)
        self.assertEqual(adapter.execute_as_tool(expression='2 plus 2'), '2 plus 2 = 4')
        self.assertEqual(adapter.process(Statement(text='2 plus the 2')).confidence, 0)
        self.assertEqual(
            adapter.execute_as_tool(expression='2 plus the 2'),
            "Error: Could not evaluate expression '2 plus the 2'",
        )


class MathematicalEvaluationTests(ChatBotTestCase):

    def setUp(self):
        super().setUp()
        self.adapter = MathematicalEvaluation(self.chatbot)

    def test_can_process(self):
        statement = Statement(text='What is 10 + 10 + 10?')
        self.assertTrue(self.adapter.can_process(statement))

    def test_can_not_process(self):
        statement = Statement(text='What is your favorite song?')
        self.assertFalse(self.adapter.can_process(statement))

    def test_addition_operator(self):
        statement = Statement(text='What is 100 + 54?')
        response = self.adapter.process(statement)
        self.assertEqual(response.text, '100 + 54 = 154')
        self.assertEqual(response.confidence, 1)

    def test_subtraction_operator(self):
        statement = Statement(text='What is 100 - 58?')
        response = self.adapter.process(statement)
        self.assertEqual(response.text, '100 - 58 = 42')
        self.assertEqual(response.confidence, 1)

    def test_multiplication_operator(self):
        statement = Statement(text='What is 100 * 20')
        response = self.adapter.process(statement)
        self.assertEqual(response.text, '100 * 20 = 2000')
        self.assertEqual(response.confidence, 1)

    def test_division_operator(self):
        statement = Statement(text='What is 100 / 20')
        response = self.adapter.process(statement)

        self.assertEqual(response.text, '100 / 20 = 5')
        self.assertEqual(response.confidence, 1)

    def test_exponent_operator(self):
        statement = Statement(text='What is 2 ^ 10')
        response = self.adapter.process(statement)
        self.assertEqual(response.text, '2 ^ 10 = 1024')
        self.assertEqual(response.confidence, 1)

    def test_parenthesized_multiplication_and_addition(self):
        statement = Statement(text='What is 100 + ( 1000 * 2 )?')
        response = self.adapter.process(statement)
        self.assertEqual(response.text, '100 + ( 1000 * 2 ) = 2100')
        self.assertEqual(response.confidence, 1)

    def test_parenthesized_with_words(self):
        statement = Statement(text='What is four plus 100 + ( 100 * 2 )?')
        response = self.adapter.process(statement)
        self.assertEqual(response.text, 'four plus 100 + ( 100 * 2 ) = 304')
        self.assertEqual(response.confidence, 1)

    def test_word_numbers_addition(self):
        statement = Statement(text='What is one hundred + four hundred?')
        response = self.adapter.process(statement)
        self.assertEqual(response.text, 'one hundred + four hundred = 500')
        self.assertEqual(response.confidence, 1)

    def test_word_division_operator(self):
        statement = Statement(text='What is 100 divided by 100?')
        response = self.adapter.process(statement)

        self.assertEqual(response.text, '100 divided by 100 = 1')
        self.assertEqual(response.confidence, 1)

    def test_large_word_division_operator(self):
        statement = Statement(text='What is one thousand two hundred four divided by one hundred?')
        response = self.adapter.process(statement)

        self.assertEqual(response.text, 'one thousand two hundred four divided by one hundred = 12.04')

        self.assertEqual(response.confidence, 1)

    def test_negative_multiplication(self):
        statement = Statement(text='What is -105 * 5')
        response = self.adapter.process(statement)
        self.assertEqual(response.text, '-105 * 5 = -525')
        self.assertEqual(response.confidence, 1)

    def test_negative_decimal_multiplication(self):
        statement = Statement(text='What is -100.5 * 20?')
        response = self.adapter.process(statement)
        self.assertEqual(response.text, '-100.5 * 20 = -2010.0')
        self.assertEqual(response.confidence, 1)

    def test_pi_constant(self):
        statement = Statement(text='What is pi plus one ?')
        response = self.adapter.process(statement)
        self.assertEqual(response.text, 'pi plus one = 4.141593')
        self.assertEqual(response.confidence, 1)

    def test_e_constant(self):
        statement = Statement(text='What is e plus one ?')
        response = self.adapter.process(statement)
        self.assertEqual(response.text, 'e plus one = 3.718281')
        self.assertEqual(response.confidence, 1)

    def test_log_function(self):
        statement = Statement(text='What is log 100 ?')
        response = self.adapter.process(statement)
        self.assertEqual(response.text, 'log 100 = 2.0')
        self.assertEqual(response.confidence, 1)

    def test_square_root_function(self):
        statement = Statement(text='What is the sqrt 144 ?')
        response = self.adapter.process(statement)
        self.assertEqual(response.text, 'sqrt 144 = 12.0')
        self.assertEqual(response.confidence, 1)
