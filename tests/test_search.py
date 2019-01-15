from tests.base_case import ChatBotTestCase
from chatterbot.conversation import Statement
from chatterbot.search import IndexedTextSearch
from chatterbot import comparisons
from chatterbot import utils


class SearchTestCase(ChatBotTestCase):

    def setUp(self):
        super().setUp()
        self.search_algorithm = IndexedTextSearch(self.chatbot)

    def test_search_no_results(self):
        """
        An exception should be raised if there is no data to return.
        """
        statement = Statement(text='What is your quest?')

        with self.assertRaises(StopIteration):
            next(self.search_algorithm.search(statement))

    def test_search_cast_to_list_no_results(self):
        """
        An empty list should be returned when the generator is
        cast to a list and there are no results to return.
        """
        statement = Statement(text='What is your quest?')

        results = list(self.search_algorithm.search(statement))

        self.assertEqual(results, [])

    def test_search_additional_parameters(self):
        """
        It should be possible to pass additional parameters in to use for searching.
        """
        self.chatbot.storage.create_many([
            Statement(text='A', conversation='test_1'),
            Statement(text='A', conversation='test_2')
        ])

        statement = Statement(text='A')

        results = list(self.search_algorithm.search(
            statement, conversation='test_1'
        ))

        self.assertIsLength(results, 1)
        self.assertEqual(results[0].text, 'A')
        self.assertEqual(results[0].conversation, 'test_1')


class SearchComparisonFunctionSynsetDistanceTests(ChatBotTestCase):
    """
    Test that the search algorithm works correctly with the
    synset distance comparison function.
    """

    def setUp(self):
        super().setUp()
        self.search_algorithm = IndexedTextSearch(
            self.chatbot,
            statement_comparison_function=comparisons.synset_distance
        )

    def test_get_closest_statement(self):
        """
        Note, the content of the in_response_to field for each of the
        test statements is only required because the logic adapter will
        filter out any statements that are not in response to a known statement.
        """
        self.chatbot.storage.create_many([
            Statement(text='This is a lovely bog.', in_response_to='This is a lovely bog.'),
            Statement(text='This is a beautiful swamp.', in_response_to='This is a beautiful swamp.'),
            Statement(text='It smells like a swamp.', in_response_to='It smells like a swamp.')
        ])

        statement = Statement(text='This is a lovely swamp.')
        results = list(self.search_algorithm.search(statement))

        self.assertIsLength(results, 1)
        self.assertEqual(results[0], 'This is a lovely bog.')
        self.assertGreater(results[0].confidence, 0)

    def test_different_punctuation(self):
        self.chatbot.storage.create_many([
            Statement(text='Who are you?'),
            Statement(text='Are you good?'),
            Statement(text='You are good')
        ])

        statement = Statement(text='Are you good')
        results = list(self.search_algorithm.search(statement))

        self.assertIsLength(results, 1)
        self.assertEqual(results[0], 'Are you good?')


class SearchComparisonFunctionSentimentComparisonTests(ChatBotTestCase):
    """
    Test that the search algorithm works correctly with the
    sentiment comparison function by using the similarity
    of sentiment polarity.
    """

    def setUp(self):
        super().setUp()
        self.search_algorithm = IndexedTextSearch(
            self.chatbot,
            statement_comparison_function=comparisons.sentiment_comparison
        )

        # Make sure the required NLTK data files are downloaded
        for function in utils.get_initialization_functions(
            self.search_algorithm,
            'compare_statements'
        ).values():
            function()

    def test_exact_input(self):
        self.chatbot.storage.create(text='What is your favorite flavor of ice cream?')
        self.chatbot.storage.create(text='I enjoy raspberry ice cream.')
        self.chatbot.storage.create(text='I am glad to hear that.')
        self.chatbot.storage.create(text='Thank you.')

        happy_statement = Statement(text='I enjoy raspberry ice cream.')
        results = list(self.search_algorithm.search(happy_statement))

        self.assertIsLength(results, 1)
        self.assertEqual(results[0].text, 'I enjoy raspberry ice cream.')
        self.assertEqual(results[0].confidence, 1)

    def test_close_input(self):
        self.chatbot.storage.create(text='What is your favorite flavor of ice cream?')
        self.chatbot.storage.create(text='I enjoy raspberry ice cream.')
        self.chatbot.storage.create(text='I am glad to hear that.')
        self.chatbot.storage.create(text='Thank you, what is yours?')
        self.chatbot.storage.create(text='Mine is chocolate.')

        happy_statement = Statement(text='I enjoy raspberry.')
        results = list(self.search_algorithm.search(happy_statement))

        self.assertIsLength(results, 1)
        self.assertEqual(results[0].text, 'I enjoy raspberry ice cream.')
        self.assertAlmostEqual(results[0].confidence, 0.75, places=1)


class SearchComparisonFunctionLevenshteinDistanceComparisonTests(ChatBotTestCase):
    """
    Test that the search algorithm works correctly with the
    Levenshtein distance comparison function.
    """

    def setUp(self):
        super().setUp()
        self.search_algorithm = IndexedTextSearch(
            self.chatbot,
            statement_comparison_function=comparisons.levenshtein_distance
        )

    def test_get_closest_statement(self):
        """
        Note, the content of the in_response_to field for each of the
        test statements is only required because the logic adapter will
        filter out any statements that are not in response to a known statement.
        """
        self.chatbot.storage.create_many([
            Statement(text='Who do you love?', in_response_to='I hear you are going on a quest?'),
            Statement(text='What is the meaning of life?', in_response_to='Yuck, black licorice jelly beans.'),
            Statement(text='I am Iron Man.', in_response_to='What... is your quest?'),
            Statement(text='What... is your quest?', in_response_to='I am Iron Man.'),
            Statement(text='Yuck, black licorice jelly beans.', in_response_to='What is the meaning of life?'),
            Statement(text='I hear you are going on a quest?', in_response_to='Who do you love?'),
        ])

        statement = Statement(text='What is your quest?')

        results = list(self.search_algorithm.search(statement))

        self.assertIsLength(results, 1)
        self.assertEqual(results[0], 'What... is your quest?')

    def test_confidence_exact_match(self):
        self.chatbot.storage.create(text='What is your quest?', in_response_to='What is your quest?')

        statement = Statement(text='What is your quest?')
        results = list(self.search_algorithm.search(statement))

        self.assertIsLength(results, 1)
        self.assertEqual(results[0].confidence, 1)

    def test_confidence_half_match(self):
        from unittest.mock import MagicMock

        # Assume that the storage adapter returns a partial match
        self.chatbot.storage.filter = MagicMock(return_value=[
            Statement(text='xxyy')
        ])

        statement = Statement(text='wwxx')
        results = list(self.search_algorithm.search(statement))

        self.assertIsLength(results, 1)
        self.assertEqual(results[0].confidence, 0.5)

    def test_confidence_no_match(self):
        from unittest.mock import MagicMock

        # Assume that the storage adapter returns a partial match
        self.search_algorithm.chatbot.storage.filter = MagicMock(return_value=[
            Statement(text='xxx', in_response_to='xxx')
        ])

        statement = Statement(text='yyy')
        results = list(self.search_algorithm.search(statement))

        self.assertIsLength(results, 0)
