from unittest import TestCase
from chatterbot.conversation import Statement


class UtilityTests(TestCase):

    def setUp(self):
        self.statement = Statement("A test statement.")

    def test_now_timestamp(self):
        """
        Tests that the correct datetime is returned
        """
        import datetime

        fmt = "%Y-%m-%d-%H-%M-%S"
        time = self.statement.now(fmt)

        self.assertEqual(time, datetime.datetime.now().strftime(fmt))

    def test_import_module(self):
        pass
