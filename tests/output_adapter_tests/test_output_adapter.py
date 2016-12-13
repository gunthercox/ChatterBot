from unittest import TestCase
from chatterbot.output import OutputAdapter


class OutputAdapterTestCase(TestCase):
    """
    This test case is for the OutputAdapter base class.
    Although this class is not intended for direct use,
    this test case ensures that exceptions requiring
    basic functionality are triggered when needed.
    """

    def setUp(self):
        super(OutputAdapterTestCase, self).setUp()
        self.adapter = OutputAdapter()

    def test_process_response(self):
        """
        The value passed in for the statement parameter should be returned.
        """
        statement = self.adapter.process_response('_', 0)
        self.assertEqual(statement, '_')
