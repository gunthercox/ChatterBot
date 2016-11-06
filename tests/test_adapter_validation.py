from chatterbot import ChatBot
from .base_case import ChatBotTestCase


class AdapterValidationTests(ChatBotTestCase):

    def setUp(self):
        super(AdapterValidationTests, self).setUp()
        self.database_path = self.chatbot.storage.database.path

    def test_invalid_storage_adapter(self):
        kwargs = self.get_kwargs()
        kwargs['storage_adapter'] = 'chatterbot.adapters.input.TerminalAdapter'
        with self.assertRaises(ChatBot.InvalidAdapterException):
            self.chatbot = ChatBot('Test Bot', **kwargs)

    def test_valid_storage_adapter(self):
        kwargs = self.get_kwargs()
        kwargs['storage_adapter'] = 'chatterbot.adapters.storage.JsonFileStorageAdapter'
        try:
            self.chatbot = ChatBot('Test Bot', **kwargs)
        except ChatBot.InvalidAdapterException:
            self.fail('Test raised InvalidAdapterException unexpectedly!')

    def test_invalid_input_adapter(self):
        kwargs = self.get_kwargs()
        kwargs['input_adapter'] = 'chatterbot.adapters.storage.JsonFileStorageAdapter'
        with self.assertRaises(ChatBot.InvalidAdapterException):
            self.chatbot = ChatBot('Test Bot', **kwargs)

    def test_valid_input_adapter(self):
        kwargs = self.get_kwargs()
        kwargs['input_adapter'] = 'chatterbot.adapters.input.TerminalAdapter'
        try:
            self.chatbot = ChatBot('Test Bot', **kwargs)
        except ChatBot.InvalidAdapterException:
            self.fail('Test raised InvalidAdapterException unexpectedly!')

    def test_invalid_output_adapter(self):
        kwargs = self.get_kwargs()
        kwargs['output_adapter'] = 'chatterbot.adapters.input.TerminalAdapter'
        with self.assertRaises(ChatBot.InvalidAdapterException):
            self.chatbot = ChatBot('Test Bot', **kwargs)

    def test_valid_output_adapter(self):
        kwargs = self.get_kwargs()
        kwargs['output_adapter'] = 'chatterbot.adapters.output.TerminalAdapter'
        try:
            self.chatbot = ChatBot('Test Bot', **kwargs)
        except ChatBot.InvalidAdapterException:
            self.fail('Test raised InvalidAdapterException unexpectedly!')

    def test_invalid_logic_adapter(self):
        kwargs = self.get_kwargs()
        kwargs['logic_adapters'] = ['chatterbot.adapters.input.TerminalAdapter']
        with self.assertRaises(ChatBot.InvalidAdapterException):
            self.chatbot = ChatBot('Test Bot', **kwargs)

    def test_valid_logic_adapter(self):
        kwargs = self.get_kwargs()
        kwargs['logic_adapters'] = ['chatterbot.adapters.logic.ClosestMatchAdapter']
        try:
            self.chatbot = ChatBot('Test Bot', **kwargs)
        except ChatBot.InvalidAdapterException:
            self.fail('Test raised InvalidAdapterException unexpectedly!')

    def test_valid_adapter_dictionary(self):
        kwargs = self.get_kwargs()
        kwargs['storage_adapter'] = {
            'import_path': 'chatterbot.adapters.storage.JsonFileStorageAdapter'
        }
        try:
            self.chatbot = ChatBot('Test Bot', **kwargs)
        except ChatBot.InvalidAdapterException:
            self.fail('Test raised InvalidAdapterException unexpectedly!')

    def test_invalid_adapter_dictionary(self):
        kwargs = self.get_kwargs()
        kwargs['storage_adapter'] = {
            'import_path': 'chatterbot.adapters.logic.ClosestMatchAdapter'
        }
        with self.assertRaises(ChatBot.InvalidAdapterException):
            self.chatbot = ChatBot('Test Bot', **kwargs)


class MultiAdapterTests(ChatBotTestCase):

    def test_add_logic_adapter(self):
        count_before = len(self.chatbot.logic.adapters)

        self.chatbot.add_logic_adapter(
            'chatterbot.adapters.logic.ClosestMatchAdapter'
        )
        self.assertEqual(len(self.chatbot.logic.adapters), count_before + 1)

    def test_insert_logic_adapter(self):
        self.chatbot.add_logic_adapter('chatterbot.adapters.logic.TimeLogicAdapter')
        self.chatbot.add_logic_adapter('chatterbot.adapters.logic.ClosestMatchAdapter')

        self.chatbot.insert_logic_adapter('chatterbot.adapters.logic.MathematicalEvaluation', 1)

        self.assertEqual(
            type(self.chatbot.logic.adapters[1]).__name__,
            'MathematicalEvaluation'
        )

    def test_remove_logic_adapter(self):
        self.chatbot.add_logic_adapter('chatterbot.adapters.logic.TimeLogicAdapter')
        self.chatbot.add_logic_adapter('chatterbot.adapters.logic.MathematicalEvaluation')

        adapter_count = len(self.chatbot.logic.adapters)

        removed = self.chatbot.remove_logic_adapter('MathematicalEvaluation')

        self.assertTrue(removed)
        self.assertEqual(len(self.chatbot.logic.adapters), adapter_count - 1)

    def test_remove_logic_adapter_not_found(self):
        self.chatbot.add_logic_adapter('chatterbot.adapters.logic.TimeLogicAdapter')

        adapter_count = len(self.chatbot.logic.adapters)

        removed = self.chatbot.remove_logic_adapter('MathematicalEvaluation')

        self.assertFalse(removed)
        self.assertEqual(len(self.chatbot.logic.adapters), adapter_count)
