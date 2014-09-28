from unittest import TestCase
from ChatBot.engram import Engram


class Tests(TestCase):

    def test_something(self):

        engram = Engram()
        response = engram.engram("hi", enable_search=False)

        self.assertTrue("hello" in response.lower())
