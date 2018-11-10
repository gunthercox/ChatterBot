from tests_django.base_case import ChatterBotTestCase
from chatterbot.ext.django_chatterbot.models import Statement
from chatterbot.input import InputAdapter


class InputIntegrationTestCase(ChatterBotTestCase):
    """
    Tests to make sure that logic adapters
    function correctly when using Django.
    """

    def test_input_adapter(self):
        adapter = InputAdapter(self.chatbot)

        statement = Statement(text='_')

        result = adapter.process_input(statement)

        self.assertEqual(result.text, '_')
