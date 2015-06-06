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

        now = datetime.datetime.now().strftime(fmt)

        self.assertEqual(time, now)

    def test_add_signature(self):
        # TODO
        self.assertTrue(True)

    def test_serializer(self):
        # TODO
        self.assertTrue(True)
