from .base_case import ChatBotTestCase


class StringInitializationTestCase(ChatBotTestCase):

    def get_kwargs(self):
        return {
            'input_adapter': 'chatterbot.input.VariableInputTypeAdapter',
            'output_adapter': 'chatterbot.output.OutputAdapter',
            'database_uri': None
        }

    def test_storage_initialized(self):
        from chatterbot.storage import SQLStorageAdapter
        self.assertTrue(isinstance(self.chatbot.storage, SQLStorageAdapter))

    def test_logic_initialized(self):
        from chatterbot.logic import BestMatch
        self.assertEqual(len(self.chatbot.logic.adapters), 1)
        self.assertTrue(isinstance(self.chatbot.logic.adapters[0], BestMatch))

    def test_input_initialized(self):
        from chatterbot.input import VariableInputTypeAdapter
        self.assertTrue(isinstance(self.chatbot.input, VariableInputTypeAdapter))

    def test_output_initialized(self):
        from chatterbot.output import OutputAdapter
        self.assertTrue(isinstance(self.chatbot.output, OutputAdapter))


class DictionaryInitializationTestCase(ChatBotTestCase):

    def get_kwargs(self):
        return {
            'storage_adapter': {
                'import_path': 'chatterbot.storage.SQLStorageAdapter',
                'database_uri': None
            },
            'input_adapter': {
                'import_path': 'chatterbot.input.VariableInputTypeAdapter'
            },
            'output_adapter': {
                'import_path': 'chatterbot.output.OutputAdapter'
            },
            'logic_adapters': [
                {
                    'import_path': 'chatterbot.logic.BestMatch',
                },
                {
                    'import_path': 'chatterbot.logic.MathematicalEvaluation',
                }
            ]
        }

    def test_storage_initialized(self):
        from chatterbot.storage import SQLStorageAdapter
        self.assertTrue(isinstance(self.chatbot.storage, SQLStorageAdapter))

    def test_logic_initialized(self):
        from chatterbot.logic import BestMatch
        from chatterbot.logic import MathematicalEvaluation
        self.assertEqual(len(self.chatbot.logic.adapters), 2)
        self.assertTrue(isinstance(self.chatbot.logic.adapters[0], BestMatch))
        self.assertTrue(isinstance(self.chatbot.logic.adapters[1], MathematicalEvaluation))

    def test_input_initialized(self):
        from chatterbot.input import VariableInputTypeAdapter
        self.assertTrue(isinstance(self.chatbot.input, VariableInputTypeAdapter))

    def test_output_initialized(self):
        from chatterbot.output import OutputAdapter
        self.assertTrue(isinstance(self.chatbot.output, OutputAdapter))
