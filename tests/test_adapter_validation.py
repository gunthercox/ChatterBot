from chatterbot import ChatBot
from chatterbot.adapters import Adapter
from .base_case import ChatBotTestCase


class AdapterValidationTests(ChatBotTestCase):

    def test_invalid_storage_adapter(self):
        kwargs = self.get_kwargs()
        kwargs['storage_adapter'] = 'chatterbot.input.TerminalAdapter'
        with self.assertRaises(Adapter.InvalidAdapterTypeException):
            self.chatbot = ChatBot('Test Bot', **kwargs)

    def test_valid_storage_adapter(self):
        kwargs = self.get_kwargs()
        kwargs['storage_adapter'] = 'chatterbot.storage.SQLStorageAdapter'
        try:
            self.chatbot = ChatBot('Test Bot', **kwargs)
        except Adapter.InvalidAdapterTypeException:
            self.fail('Test raised InvalidAdapterException unexpectedly!')

    def test_invalid_input_adapter(self):
        kwargs = self.get_kwargs()
        kwargs['input_adapter'] = 'chatterbot.storage.SQLStorageAdapter'
        with self.assertRaises(Adapter.InvalidAdapterTypeException):
            self.chatbot = ChatBot('Test Bot', **kwargs)

    def test_valid_input_adapter(self):
        kwargs = self.get_kwargs()
        kwargs['input_adapter'] = 'chatterbot.input.TerminalAdapter'
        try:
            self.chatbot = ChatBot('Test Bot', **kwargs)
        except Adapter.InvalidAdapterTypeException:
            self.fail('Test raised InvalidAdapterException unexpectedly!')

    def test_invalid_output_adapter(self):
        kwargs = self.get_kwargs()
        kwargs['output_adapter'] = 'chatterbot.input.TerminalAdapter'
        with self.assertRaises(Adapter.InvalidAdapterTypeException):
            self.chatbot = ChatBot('Test Bot', **kwargs)

    def test_valid_output_adapter(self):
        kwargs = self.get_kwargs()
        kwargs['output_adapter'] = 'chatterbot.output.TerminalAdapter'
        try:
            self.chatbot = ChatBot('Test Bot', **kwargs)
        except Adapter.InvalidAdapterTypeException:
            self.fail('Test raised InvalidAdapterException unexpectedly!')

    def test_invalid_logic_adapter(self):
        kwargs = self.get_kwargs()
        kwargs['logic_adapters'] = ['chatterbot.input.TerminalAdapter']
        with self.assertRaises(Adapter.InvalidAdapterTypeException):
            self.chatbot = ChatBot('Test Bot', **kwargs)

    def test_valid_logic_adapter(self):
        kwargs = self.get_kwargs()
        kwargs['logic_adapters'] = ['chatterbot.logic.BestMatch']
        try:
            self.chatbot = ChatBot('Test Bot', **kwargs)
        except Adapter.InvalidAdapterTypeException:
            self.fail('Test raised InvalidAdapterException unexpectedly!')

    def test_valid_adapter_dictionary(self):
        kwargs = self.get_kwargs()
        kwargs['storage_adapter'] = {
            'import_path': 'chatterbot.storage.SQLStorageAdapter'
        }
        try:
            self.chatbot = ChatBot('Test Bot', **kwargs)
        except Adapter.InvalidAdapterTypeException:
            self.fail('Test raised InvalidAdapterException unexpectedly!')

    def test_invalid_adapter_dictionary(self):
        kwargs = self.get_kwargs()
        kwargs['storage_adapter'] = {
            'import_path': 'chatterbot.logic.BestMatch'
        }
        with self.assertRaises(Adapter.InvalidAdapterTypeException):
            self.chatbot = ChatBot('Test Bot', **kwargs)
