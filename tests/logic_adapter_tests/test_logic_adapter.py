from unittest import TestCase
from chatterbot.logic import LogicAdapter


class LogicAdapterTestCase(TestCase):
    """
    This test case is for the LogicAdapter base class.
    Although this class is not intended for direct use,
    this test case ensures that exceptions requiring
    basic functionality are triggered when needed.
    """

    def setUp(self):
        super(LogicAdapterTestCase, self).setUp()
        self.adapter = LogicAdapter()

    def test_class_name(self):
        """
        Test that the logic adapter can return its own class name.
        """
        self.assertEqual(self.adapter.class_name, 'LogicAdapter')

    def test_can_process(self):
        """
        This method should return true by default.
        """
        self.assertTrue(self.adapter.can_process(''))

    def test_process(self):
        with self.assertRaises(LogicAdapter.AdapterMethodNotImplementedError):
            self.adapter.process('')

    def test_set_statement_comparison_function_string(self):
        adapter = LogicAdapter(
            statement_comparison_function='chatterbot.comparisons.levenshtein_distance'
        )
        self.assertTrue(callable(adapter.compare_statements))

    def test_set_statement_comparison_function_callable(self):
        from chatterbot.comparisons import levenshtein_distance
        adapter = LogicAdapter(
            statement_comparison_function=levenshtein_distance
        )
        self.assertTrue(callable(adapter.compare_statements))

    def test_set_response_selection_method_string(self):
        adapter = LogicAdapter(
            response_selection_method='chatterbot.response_selection.get_first_response'
        )
        self.assertTrue(callable(adapter.select_response))

    def test_set_response_selection_method_callable(self):
        from chatterbot.response_selection import get_first_response
        adapter = LogicAdapter(
            response_selection_method=get_first_response
        )
        self.assertTrue(callable(adapter.select_response))
