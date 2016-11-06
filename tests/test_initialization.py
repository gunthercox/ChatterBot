from .base_case import ChatBotTestCase


class StringInitalizationTestCase(ChatBotTestCase):

    def get_kwargs(self):
        return {
            'input_adapter': 'chatterbot.adapters.input.VariableInputTypeAdapter',
            'output_adapter': 'chatterbot.adapters.output.OutputFormatAdapter',
            'database': self.create_test_data_directory(),
            'silence_performance_warning': True
        }

    def test_storage_initialized(self):
        from chatterbot.adapters.storage import JsonFileStorageAdapter
        self.assertTrue(isinstance(self.chatbot.storage, JsonFileStorageAdapter))

    def test_logic_initialized(self):
        from chatterbot.adapters.logic import ClosestMatchAdapter
        self.assertTrue(isinstance(self.chatbot.logic.adapters[1], ClosestMatchAdapter))

    def test_input_initialized(self):
        from chatterbot.adapters.input import VariableInputTypeAdapter
        self.assertTrue(isinstance(self.chatbot.input, VariableInputTypeAdapter))

    def test_output_initialized(self):
        from chatterbot.adapters.output import OutputFormatAdapter
        self.assertTrue(isinstance(self.chatbot.output, OutputFormatAdapter))


class DictionaryInitalizationTestCase(ChatBotTestCase):

    def get_kwargs(self):
        return {
            'storage_adapter': {
                'import_path': 'chatterbot.adapters.storage.JsonFileStorageAdapter',
                'database': self.create_test_data_directory(),
                'silence_performance_warning': True
            },

            'input_adapter': {
                'import_path': 'chatterbot.adapters.input.VariableInputTypeAdapter'
            },
            'output_adapter': {
                 'import_path': 'chatterbot.adapters.output.OutputFormatAdapter'
            },
            'logic_adapters': [
                {
                    'import_path': 'chatterbot.adapters.logic.ClosestMatchAdapter',
                },
                {
                    'import_path': 'chatterbot.adapters.logic.MathematicalEvaluation',
                }
            ]
        }

    def test_storage_initialized(self):
        from chatterbot.adapters.storage import JsonFileStorageAdapter
        self.assertTrue(isinstance(self.chatbot.storage, JsonFileStorageAdapter))

    def test_logic_initialized(self):
        from chatterbot.adapters.logic import ClosestMatchAdapter
        from chatterbot.adapters.logic import MathematicalEvaluation
        self.assertTrue(isinstance(self.chatbot.logic.adapters[1], ClosestMatchAdapter))
        self.assertTrue(isinstance(self.chatbot.logic.adapters[2], MathematicalEvaluation))

    def test_input_initialized(self):
        from chatterbot.adapters.input import VariableInputTypeAdapter
        self.assertTrue(isinstance(self.chatbot.input, VariableInputTypeAdapter))

    def test_output_initialized(self):
        from chatterbot.adapters.output import OutputFormatAdapter
        self.assertTrue(isinstance(self.chatbot.output, OutputFormatAdapter))