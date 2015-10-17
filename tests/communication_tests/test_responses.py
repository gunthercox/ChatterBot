from unittest import TestCase
from chatterbot.conversation import Response, Signature


class ResponseTests(TestCase):

    def setUp(self):
        self.response = Response("A test response.")

    def test_add_signature(self):
        signature = Signature("Gunther Cox")
        self.response.add_signature(signature)
        self.assertIn(signature, self.response.signatures)

