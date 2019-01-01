from tests.base_case import ChatBotTestCase
from chatterbot.logic import LogicAdapter
from chatterbot.conversation import Statement


class LogicAdapterTestCase(ChatBotTestCase):
    """
    This test case is for the LogicAdapter base class.
    Although this class is not intended for direct use,
    this test case ensures that exceptions requiring
    basic functionality are triggered when needed.
    """

    def setUp(self):
        super().setUp()
        self.adapter = LogicAdapter(self.chatbot)

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

    def test_get_default_response(self):
        response = self.adapter.get_default_response(Statement(text='...'))

        self.assertEqual(response.text, '...')

    def test_get_default_response_from_options(self):
        self.adapter.default_responses = [
            Statement(text='The default')
        ]
        response = self.adapter.get_default_response(Statement(text='...'))

        self.assertEqual(response.text, 'The default')

    def test_get_default_response_from_database(self):
        self.chatbot.storage.create(text='The default')

        response = self.adapter.get_default_response(Statement(text='...'))

        self.assertEqual(response.text, 'The default')
