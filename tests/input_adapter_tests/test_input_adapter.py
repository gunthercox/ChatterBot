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
            self.adapter.process_input()

    def test_process_response_statement(self):
        with self.assertRaises(InputAdapter.AdapterMethodNotImplementedError):
            self.adapter.process_input_statement()

    def test_process_response_statement_initialized(self):
        self.adapter.chatbot = self.chatbot
        self.adapter.process_input = lambda *args, **kwargs: Statement('Hi')
        response = self.adapter.process_input_statement()
        self.assertEqual(response, 'Hi')
