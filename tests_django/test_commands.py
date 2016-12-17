from django.core.management import call_command
from django.test import TestCase
from django.utils.six import StringIO
from chatterbot.ext.django_chatterbot.models import Statement


class TrainCommandTestCase(TestCase):

    def test_command_output(self):
        out = StringIO()
        call_command('train', stdout=out)
        self.assertIn('ChatterBot trained', out.getvalue())

    def test_command_data_argument(self):
        out = StringIO()
        statements_before = Statement.objects.exists()
        call_command('train', stdout=out)
        statements_after = Statement.objects.exists()

        self.assertFalse(statements_before)
        self.assertTrue(statements_after)
