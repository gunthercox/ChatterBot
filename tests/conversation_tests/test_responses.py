from unittest import TestCase
from chatterbot.conversation import Response


class ResponseTests(TestCase):

    def setUp(self):
        self.response = Response("A test response.")

