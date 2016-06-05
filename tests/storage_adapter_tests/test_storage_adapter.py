from unittest import TestCase
from chatterbot.adapters.storage import StorageAdapter
from chatterbot.conversation import Statement, Response

class StorageAdapterTestCase(TestCase):
    """
    This test case is for the StorageAdapter base class.
    Although this class is not intended for direct use,
    this test case ensures that exceptions requiring
    basic functionality are triggered when needed.
    """

    def setUp(self):
        super(StorageAdapterTestCase, self).setUp()
        self.adapter = StorageAdapter()

    def test_count(self):
        with self.assertRaises(StorageAdapter.AdapterMethodNotImplementedError):
            self.adapter.count()

    def test_find(self):
        with self.assertRaises(StorageAdapter.AdapterMethodNotImplementedError):
            self.adapter.find("")

    def test_filter(self):
        with self.assertRaises(StorageAdapter.AdapterMethodNotImplementedError):
            self.adapter.filter()

    def test_remove(self):
        with self.assertRaises(StorageAdapter.AdapterMethodNotImplementedError):
            self.adapter.remove("")

    def test_update(self):
        with self.assertRaises(StorageAdapter.AdapterMethodNotImplementedError):
            self.adapter.update("")

    def test_get_random(self):
        with self.assertRaises(StorageAdapter.AdapterMethodNotImplementedError):
            self.adapter.get_random()

    def test_get_response_statements(self):
        """
        Test that we are able to get a list of only statements
        that are known to be in response to another statement.
        """
        statement_list = [
            Statement("What... is your quest?"),
            Statement("This is a phone."),
            Statement("A what?", in_response_to=[Response("This is a phone.")]),
            Statement("A phone.", in_response_to=[Response("A what?")])
        ]

        # TODO Add the above statements to the database

        responses = self.adapter.get_response_statements()

        self.assertEqual(len(responses), 2)
        self.assertIn("This is a phone.", responses)
        self.assertIn("A what?", responses)

    def test_drop(self):
        with self.assertRaises(StorageAdapter.AdapterMethodNotImplementedError):
            self.adapter.drop()
