from django.test import TestCase
from chatterbot.ext.django_chatterbot.models import Statement


class OutputIntegrationTestCase(TestCase):
    """
    Tests to make sure that output adapters
    function correctly when using Django.
    """

    def test_output_adapter(self):
        from chatterbot.output import OutputAdapter

        adapter = OutputAdapter()

        statement = Statement(text='_')
        result = adapter.process_response(statement)

        self.assertEqual(result.text, '_')
