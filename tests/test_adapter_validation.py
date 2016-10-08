from chatterbot import ChatBot
from .base_case import ChatBotTestCase


class AdapterValidationTests(ChatBotTestCase):

    def setUp(self):
        super(AdapterValidationTests, self).setUp()
        self.database_path = self.chatbot.storage.database.path

    def test_invalid_storage_adapter(self):
        with self.assertRaises(ChatBot.InvalidAdapterException):
            self.chatbot = ChatBot(
                'Test Bot',
                storage_adapter='chatterbot.adapters.input.TerminalAdapter',
                database=self.database_path,
                silence_performance_warning=True
            )

    def test_valid_storage_adapter(self):
        try:
            self.chatbot = ChatBot(
                'Test Bot',
                storage_adapter='chatterbot.adapters.storage.JsonFileStorageAdapter',
                database=self.database_path
            )
        except ChatBot.InvalidAdapterException:
            self.fail('Test raised InvalidAdapterException unexpectedly!')

    def test_invalid_input_adapter(self):
        with self.assertRaises(ChatBot.InvalidAdapterException):
            self.chatbot = ChatBot(
                'Test Bot',
                input_adapter='chatterbot.adapters.storage.JsonFileStorageAdapter',
                database=self.database_path
            )

    def test_valid_input_adapter(self):
        try:
            self.chatbot = ChatBot(
                'Test Bot',
                input_adapter='chatterbot.adapters.input.TerminalAdapter',
                database=self.database_path
            )
        except ChatBot.InvalidAdapterException:
            self.fail('Test raised InvalidAdapterException unexpectedly!')

    def test_invalid_output_adapter(self):
        with self.assertRaises(ChatBot.InvalidAdapterException):
            self.chatbot = ChatBot(
                'Test Bot',
                output_adapter='chatterbot.adapters.input.TerminalAdapter',
                database=self.database_path
            )

    def test_valid_output_adapter(self):
        try:
            self.chatbot = ChatBot(
                'Test Bot',
                output_adapter='chatterbot.adapters.output.TerminalAdapter',
                database=self.database_path
            )
        except ChatBot.InvalidAdapterException:
            self.fail('Test raised InvalidAdapterException unexpectedly!')

    def test_invalid_logic_adapter(self):
        with self.assertRaises(ChatBot.InvalidAdapterException):
            self.chatbot = ChatBot(
                'Test Bot',
                logic_adapters=[
                    'chatterbot.adapters.input.TerminalAdapter',
                ],
                database=self.database_path
            )

    def test_valid_logic_adapter(self):
        try:
            self.chatbot = ChatBot(
                'Test Bot',
                logic_adapters=[
                    'chatterbot.adapters.logic.ClosestMatchAdapter'
                ],
                database=self.database_path
            )
        except ChatBot.InvalidAdapterException:
            self.fail('Test raised InvalidAdapterException unexpectedly!')


class MultiAdapterTests(ChatBotTestCase):

    def test_add_logic_adapter(self):
        count_before = len(self.chatbot.logic.adapters)

        self.chatbot.add_adapter(
            'chatterbot.adapters.logic.ClosestMatchAdapter'
        )
        self.assertEqual(len(self.chatbot.logic.adapters), count_before + 1)

    def test_insert_logic_adapter(self):
        self.chatbot.add_adapter('chatterbot.adapters.logic.TimeLogicAdapter')
        self.chatbot.add_adapter('chatterbot.adapters.logic.ClosestMatchAdapter')

        self.chatbot.insert_logic_adapter('chatterbot.adapters.logic.MathematicalEvaluation', 1)

        self.assertEqual(
            type(self.chatbot.logic.adapters[1]).__name__,
            'MathematicalEvaluation'
        )

    def test_remove_logic_adapter(self):
        self.chatbot.add_adapter('chatterbot.adapters.logic.TimeLogicAdapter')
        self.chatbot.add_adapter('chatterbot.adapters.logic.MathematicalEvaluation')

        adapter_count = len(self.chatbot.logic.adapters)

        removed = self.chatbot.remove_logic_adapter('MathematicalEvaluation')

        self.assertTrue(removed)
        self.assertEqual(len(self.chatbot.logic.adapters), adapter_count - 1)

    def test_remove_logic_adapter_not_found(self):
        self.chatbot.add_adapter('chatterbot.adapters.logic.TimeLogicAdapter')

        adapter_count = len(self.chatbot.logic.adapters)

        removed = self.chatbot.remove_logic_adapter('MathematicalEvaluation')

        self.assertFalse(removed)
        self.assertEqual(len(self.chatbot.logic.adapters), adapter_count)
