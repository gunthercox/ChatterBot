from chatterbot import ChatBot
from .base_case import ChatBotTestCase


class AdapterValidationTests(ChatBotTestCase):

    def test_invalid_storage_adapter(self):
        with self.assertRaises(ChatBot.InvalidAdapterException):
            self.chatbot = ChatBot(
                "Test Bot",
                storage_adapter="chatterbot.adapters.input.TerminalAdapter",
                database=self.database_path
            )

    def test_valid_storage_adapter(self):
        try:
            self.chatbot = ChatBot(
                "Test Bot",
                storage_adapter="chatterbot.adapters.storage.JsonDatabaseAdapter",
                database=self.database_path
            )
        except ChatBot.InvalidAdapterException:
            self.fail("Test raised InvalidAdapterException unexpectedly!")

    def test_invalid_input_adapter(self):
        with self.assertRaises(ChatBot.InvalidAdapterException):
            self.chatbot = ChatBot(
                "Test Bot",
                input_adapter="chatterbot.adapters.storage.JsonDatabaseAdapter",
                database=self.database_path
            )

    def test_valid_input_adapter(self):
        try:
            self.chatbot = ChatBot(
                "Test Bot",
                input_adapter="chatterbot.adapters.input.TerminalAdapter",
                database=self.database_path
            )
        except ChatBot.InvalidAdapterException:
            self.fail("Test raised InvalidAdapterException unexpectedly!")

    def test_invalid_output_adapter(self):
        with self.assertRaises(ChatBot.InvalidAdapterException):
            self.chatbot = ChatBot(
                "Test Bot",
                output_adapter="chatterbot.adapters.input.TerminalAdapter",
                database=self.database_path
            )

    def test_valid_output_adapter(self):
        try:
            self.chatbot = ChatBot(
                "Test Bot",
                output_adapter="chatterbot.adapters.output.TerminalAdapter",
                database=self.database_path
            )
        except ChatBot.InvalidAdapterException:
            self.fail("Test raised InvalidAdapterException unexpectedly!")

    def test_invalid_logic_adapter(self):
        with self.assertRaises(ChatBot.InvalidAdapterException):
            self.chatbot = ChatBot(
                "Test Bot",
                logic_adapter="chatterbot.adapters.input.TerminalAdapter",
                database=self.database_path
            )

    def test_valid_logic_adapter(self):
        try:
            self.chatbot = ChatBot(
                "Test Bot",
                logic_adapters=[
                    "chatterbot.adapters.logic.ClosestMatchAdapter"
                ],
                database=self.database_path
            )
        except ChatBot.InvalidAdapterException:
            self.fail("Test raised InvalidAdapterException unexpectedly!")


class MultiAdapterTests(ChatBotTestCase):

    def test_add_logic_adapter(self):
        count_before = len(self.chatbot.logic.adapters)

        self.chatbot.add_adapter(
            "chatterbot.adapters.logic.ClosestMatchAdapter"
        )
        self.assertEqual(len(self.chatbot.logic.adapters), count_before + 1)
