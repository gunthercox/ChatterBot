from unittest import TestCase

from chatterbot.utils.module_loading import import_module
from chatterbot.utils.chronology import timestamp


class UtilityTests(TestCase):

    def test_timestamp(self):
        """
        Tests that the correct datetime is returned
        """
        import datetime

        fmt = "%Y-%m-%d-%H-%M-%S"
        time = timestamp(fmt)

        self.assertEqual(time, datetime.datetime.now().strftime(fmt))

    def test_import_module(self):
        pass
