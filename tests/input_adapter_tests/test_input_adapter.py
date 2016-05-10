from unittest import TestCase
from chatterbot.adapters.input import InputAdapter

class InputAdapterTestCase(TestCase):
    """
    This test case is for the InputAdapter base class.
    Although this class is not intended for direct use,
    this test case ensures that exceptions requiring
    basic functionality are triggered when needed.
    """

    def setUp(self):
        super(InputAdapterTestCase, self).setUp()
        self.adapter = InputAdapter()

    def test_process_response(self):
        with self.assertRaises(InputAdapter.AdapterMethodNotImplementedError):
            self.adapter.process_input()
