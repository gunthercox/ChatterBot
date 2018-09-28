from tests_django.base_case import ChatterBotTestCase
from chatterbot.ext.django_chatterbot.models import Statement


class InputIntegrationTestCase(ChatterBotTestCase):
    """
    Tests to make sure that logic adapters
    function correctly when using Django.
    """

    def test_variable_type_input_adapter(self):
        from chatterbot.input import VariableInputTypeAdapter

        adapter = VariableInputTypeAdapter(self.chatbot)

        statement = Statement(text='_')

        result = adapter.process_input(statement)

        self.assertEqual(result.text, '_')
