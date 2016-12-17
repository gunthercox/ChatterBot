from unittest import TestCase
from chatterbot.storage import StorageAdapter
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
            self.adapter.find('')

    def test_filter(self):
        with self.assertRaises(StorageAdapter.AdapterMethodNotImplementedError):
            self.adapter.filter()

    def test_remove(self):
        with self.assertRaises(StorageAdapter.AdapterMethodNotImplementedError):
            self.adapter.remove('')

    def test_update(self):
        with self.assertRaises(StorageAdapter.AdapterMethodNotImplementedError):
            self.adapter.update('')

    def test_get_random(self):
        with self.assertRaises(StorageAdapter.AdapterMethodNotImplementedError):
            self.adapter.get_random()

    def test_get_response_statements(self):
        with self.assertRaises(StorageAdapter.AdapterMethodNotImplementedError):
            self.adapter.get_response_statements()

    def test_drop(self):
        with self.assertRaises(StorageAdapter.AdapterMethodNotImplementedError):
            self.adapter.drop()
