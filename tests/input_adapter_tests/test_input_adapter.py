from tests.base_case import ChatBotTestCase
from chatterbot.conversation import Statement
from chatterbot.input import InputAdapter


class InputAdapterTestCase(ChatBotTestCase):
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
            self.adapter.process_input(
                'test statement',
                'test conversation'
            )
