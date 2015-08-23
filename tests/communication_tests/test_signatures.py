from unittest import TestCase
from chatterbot.conversation import Signature


class SignatureTests(TestCase):

    def setUp(self):
        self.signature = Signature("Gunther Cox")

    def test_add_timestamp(self):
        """
        Tests that the correct timestamp is returned.
        """
        import datetime

        fmt = "%Y-%m-%d-%H-%M-%S"
        time = self.signature.create_timestamp(fmt)

        now = datetime.datetime.now().strftime(fmt)

        self.assertEqual(time, now)

    def test_serializer(self):
        data = self.signature.serialize()
        self.assertEqual(self.signature.name, data["name"])
        self.assertEqual(self.signature.time, data["time"])

