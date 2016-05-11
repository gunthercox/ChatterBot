from unittest import TestCase
from chatterbot.adapters.logic import LogicAdapter

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

    def test_can_process(self):
        """
        This method should return true by default.
        """
        self.assertTrue(self.adapter.can_process(""))

    def test_process(self):
        with self.assertRaises(LogicAdapter.AdapterMethodNotImplementedError):
            self.adapter.process("")
