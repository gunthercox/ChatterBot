from unittest import TestCase
from chatterbot.storage import StorageAdapter


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

    def test_filter(self):
        with self.assertRaises(StorageAdapter.AdapterMethodNotImplementedError):
            self.adapter.filter()

    def test_remove(self):
        with self.assertRaises(StorageAdapter.AdapterMethodNotImplementedError):
            self.adapter.remove('')

    def test_create(self):
        with self.assertRaises(StorageAdapter.AdapterMethodNotImplementedError):
            self.adapter.create()

    def test_update(self):
        with self.assertRaises(StorageAdapter.AdapterMethodNotImplementedError):
            self.adapter.update('')

    def test_get_random(self):
        with self.assertRaises(StorageAdapter.AdapterMethodNotImplementedError):
            self.adapter.get_random()

    def test_drop(self):
        with self.assertRaises(StorageAdapter.AdapterMethodNotImplementedError):
            self.adapter.drop()
