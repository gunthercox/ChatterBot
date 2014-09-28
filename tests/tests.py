from unittest import TestCase
from ChatBot.engram import Engram


class Tests(TestCase):

    def test_something(self):

        engram = Engram(enable_search=False)
        response = engram.engram("hi")

        self.assertTrue("hello" in response.lower())
