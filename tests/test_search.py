from tests.base_case import ChatBotTestCase
from chatterbot.conversation import Statement
from chatterbot.search import TextSearch, IndexedTextSearch
from chatterbot import comparisons


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
        self._create_many_with_search_text([
            Statement(text='B', in_response_to='A', conversation='test_1'),
            Statement(text='B', in_response_to='A', conversation='test_2')
        ])

        statement = Statement(text='A')

        results = list(self.search_algorithm.search(
            statement, conversation='test_1'
        ))

        self.assertIsLength(results, 1)
        self.assertEqual(results[0].text, 'B')
        self.assertEqual(results[0].conversation, 'test_1')


class IndexedTextSearchComparisonFunctionSpacySimilarityTests(ChatBotTestCase):
    """
    Test that the search algorithm works correctly with the
    spacy similarity comparison function.
    """

    def setUp(self):
        super().setUp()
        self.search_algorithm = IndexedTextSearch(
            self.chatbot,
            statement_comparison_function=comparisons.SpacySimilarity
        )

    def test_get_closest_statement(self):
        """
        Note, the content of the in_response_to field for each of the
        test statements is only required because the logic adapter will
        filter out any statements that are not in response to a known statement.
        """
        self._create_many_with_search_text([
            Statement(text='This is a lovely bog.', in_response_to='This is a lovely bog.'),
            Statement(text='This is a beautiful swamp.', in_response_to='This is a beautiful swamp.'),
            Statement(text='It smells like a swamp.', in_response_to='It smells like a swamp.')
        ])

        statement = Statement(text='This is a lovely swamp.')
        results = list(self.search_algorithm.search(statement))

        self.assertIsLength(results, 2)
        self.assertEqual(results[1].text, 'This is a beautiful swamp.')
        self.assertGreater(results[1].confidence, 0)

    def test_different_punctuation(self):
        self._create_many_with_search_text([
            Statement(text='A', in_response_to='Who are you?'),
            Statement(text='B', in_response_to='Are you good?'),
            Statement(text='C', in_response_to='You are good')
        ])

        statement = Statement(text='Are you good')
        results = list(self.search_algorithm.search(statement))

        self.assertEqual(len(results), 2, msg=[r.search_text for r in results])
        # Note: the last statement in the list always has the highest confidence
        self.assertEqual(results[-1].text, 'B')


class IndexedTextSearchComparisonFunctionLevenshteinDistanceComparisonTests(ChatBotTestCase):
    """
    Test that the search algorithm works correctly with the
    Levenshtein distance comparison function.
    """

    def setUp(self):
        super().setUp()
        self.search_algorithm = IndexedTextSearch(
            self.chatbot,
            statement_comparison_function=comparisons.LevenshteinDistance
        )

    def test_get_closest_statement(self):
        """
        Note, the content of the in_response_to field for each of the
        test statements is only required because the search process will
        filter out any statements that are not in response to something.
        """
        self._create_many_with_search_text([
            Statement(text='A', in_response_to='What is the meaning of life?'),
            Statement(text='B', in_response_to='I am Iron Man.'),
            Statement(text='C', in_response_to='What... is your quest?'),
            Statement(text='D', in_response_to='Yuck, black licorice jelly beans.'),
            Statement(text='E', in_response_to='I hear you are going on a quest?'),
        ])

        statement = Statement(text='What is your quest?')

        results = list(self.search_algorithm.search(statement))

        self.assertEqual(len(results), 2, msg=[r.in_response_to for r in results])
        self.assertEqual(results[1].in_response_to, 'What... is your quest?')

    def test_confidence_exact_match(self):
        self._create_with_search_text(text='What is your quest?', in_response_to='What is your quest?')

        statement = Statement(text='What is your quest?')
        results = list(self.search_algorithm.search(statement))

        self.assertIsLength(results, 1)
        self.assertEqual(results[0].confidence, 1)

    def test_confidence_half_match(self):
        from unittest.mock import MagicMock

        # Assume that the storage adapter returns a partial match
        self.chatbot.storage.filter = MagicMock(return_value=[
            Statement(text='', in_response_to='xxyy')
        ])

        statement = Statement(text='wwxx')
        results = list(self.search_algorithm.search(statement))

        self.assertIsLength(results, 1)
        self.assertEqual(results[0].confidence, 0.5, msg=results)

    def test_confidence_no_match(self):
        from unittest.mock import MagicMock

        # Assume that the storage adapter returns a partial match
        self.search_algorithm.chatbot.storage.filter = MagicMock(return_value=[
            Statement(text='xxx', in_response_to='xxx')
        ])

        statement = Statement(text='yyy')
        results = list(self.search_algorithm.search(statement))

        self.assertIsLength(results, 0)


class TextSearchComparisonFunctionSpacySimilarityTests(ChatBotTestCase):
    """
    Test that the search algorithm works correctly with the
    spacy similarity comparison function.
    """

    def setUp(self):
        super().setUp()
        self.search_algorithm = TextSearch(
            self.chatbot,
            statement_comparison_function=comparisons.SpacySimilarity
        )

    def test_get_closest_statement(self):
        """
        Note, the content of the in_response_to field for each of the
        test statements is only required because the logic adapter will
        filter out any statements that are not in response to a known statement.
        """
        self._create_many_with_search_text([
            Statement(text='This is a lovely bog.', in_response_to='This is a lovely bog.'),
            Statement(text='This is a beautiful swamp.', in_response_to='This is a beautiful swamp.'),
            Statement(text='It smells like a swamp.', in_response_to='It smells like a swamp.')
        ])

        statement = Statement(text='This is a lovely swamp.')
        results = list(self.search_algorithm.search(statement))

        self.assertIsLength(results, 2)
        self.assertEqual(results[-1].text, 'This is a beautiful swamp.')
        self.assertGreater(results[-1].confidence, 0)

    def test_different_punctuation(self):
        self._create_many_with_search_text([
            Statement(text='A', in_response_to='Who are you?'),
            Statement(text='B', in_response_to='Are you good?'),
            Statement(text='C', in_response_to='You are good')
        ])

        statement = Statement(text='Are you good')
        results = list(self.search_algorithm.search(statement))

        self.assertEqual(len(results), 2)
        # Note: the last statement in the list always has the highest confidence
        self.assertEqual(results[-1].in_response_to, 'Are you good?')


class TextSearchComparisonFunctionLevenshteinDistanceComparisonTests(ChatBotTestCase):
    """
    Test that the search algorithm works correctly with the
    Levenshtein distance comparison function.
    """

    def setUp(self):
        super().setUp()
        self.search_algorithm = TextSearch(
            self.chatbot,
            statement_comparison_function=comparisons.LevenshteinDistance
        )

    def test_get_closest_statement(self):
        """
        Note, the content of the in_response_to field for each of the
        test statements is only required because the search process will
        filter out any statements that are not in response to something.
        """
        self._create_many_with_search_text([
            Statement(text='A', in_response_to='What is the meaning of life?'),
            Statement(text='B', in_response_to='I am Iron Man.'),
            Statement(text='C', in_response_to='What... is your quest?'),
            Statement(text='D', in_response_to='Yuck, black licorice jelly beans.'),
            Statement(text='E', in_response_to='I hear you are going on a quest?'),
        ])

        statement = Statement(text='What is your quest?')

        results = list(self.search_algorithm.search(statement))

        self.assertEqual(len(results), 2)
        self.assertEqual(results[-1].in_response_to, 'What... is your quest?', msg=results[-1].confidence)

    def test_confidence_exact_match(self):
        self._create_with_search_text(text='What is your quest?', in_response_to='What is your quest?')

        statement = Statement(text='What is your quest?')
        results = list(self.search_algorithm.search(statement))

        self.assertIsLength(results, 1)
        self.assertEqual(results[0].confidence, 1)

    def test_confidence_half_match(self):
        from unittest.mock import MagicMock

        # Assume that the storage adapter returns a partial match
        self.chatbot.storage.filter = MagicMock(return_value=[
            Statement(text='', in_response_to='xxyy')
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
