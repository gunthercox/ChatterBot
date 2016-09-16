from chatterbot import ChatBot
from .base_case import ChatBotTestCase


class AdapterValidationTests(ChatBotTestCase):

    def setUp(self):
        super(AdapterValidationTests, self).setUp()
        self.database_path = self.chatbot.storage.database.path
        self.storage_json = 'chatterbot.adapters.storage.JsonFileStorageAdapter'
        self.input_terminal = 'chatterbot.adapters.input.TerminalAdapter'
        self.logic_matcher = 'chatterbot.adapters.logic.ClosestMatchAdapter'
        self.output_terminal = 'chatterbot.adapters.output.TerminalAdapter'

    def test_invalid_storage_adapter(self):
        storage_adapter = {'adapter_class': self.input_terminal,
                           'database': self.database_path}
        with self.assertRaises(ChatBot.InvalidAdapterException):
            self.chatbot = ChatBot('Test Bot', storage_adapter=storage_adapter)

    def test_valid_storage_adapter(self):
        storage_adapter = {'adapter_class': self.storage_json,
                           'databas': self.database_path}
        try:
            self.chatbot = ChatBot('Test Bot', storage_adapter=storage_adapter)
        except ChatBot.InvalidAdapterException:
            self.fail('Test raised InvalidAdapterException unexpectedly!')

    def test_invalid_input_adapter(self):
        input_adapter = {'adapter_class': self.storage_json,
                         'databas': self.database_path}
        with self.assertRaises(ChatBot.InvalidAdapterException):
            self.chatbot = ChatBot('Test Bot', input_adapter=input_adapter)

    def test_valid_input_adapter(self):
        input_adapter = {'adapter_class': self.input_terminal,
                         'database': self.database_path}
        try:
            self.chatbot = ChatBot('Test Bot', input_adapter=input_adapter)
        except ChatBot.InvalidAdapterException:
            self.fail('Test raised InvalidAdapterException unexpectedly!')

    def test_invalid_output_adapter(self):
        output_adapter = {'adapter_class': self.input_terminal,
                          'database': self.database_path}
        with self.assertRaises(ChatBot.InvalidAdapterException):
            self.chatbot = ChatBot('Test Bot', output_adapter=output_adapter)

    def test_valid_output_adapter(self):
        output_adapter = {'adapter_class': self.output_terminal,
                          'database': self.database_path}

        try:
            self.chatbot = ChatBot('Test Bot', output_adapter=output_adapter)
        except ChatBot.InvalidAdapterException:
            self.fail('Test raised InvalidAdapterException unexpectedly!')

    def test_invalid_logic_adapter(self):
        logic_adapter = {'adpater_class': self.input_terminal,
                         'database': self.database_path}
        with self.assertRaises(ChatBot.InvalidAdapterException):
            self.chatbot = ChatBot('Test Bot', logic_adapters=[logic_adapter])

    def test_valid_logic_adapter(self):
        logic_adapter = {'adpater_class': self.logic_matcher,
                         'database': self.database_path}
        try:
            self.chatbot = ChatBot('Test Bot', logic_adapters=[logic_adapter])
        except ChatBot.InvalidAdapterException:
            self.fail('Test raised InvalidAdapterException unexpectedly!')


class MultiAdapterTests(ChatBotTestCase):

    def test_add_logic_adapter(self):
        count_before = len(self.chatbot.logic.adapters)

        self.chatbot.add_adapter(
            'chatterbot.adapters.logic.ClosestMatchAdapter'
        )
        self.assertEqual(len(self.chatbot.logic.adapters), count_before + 1)
