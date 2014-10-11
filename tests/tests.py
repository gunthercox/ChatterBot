from unittest import TestCase
from ChatBot.engram import Engram


class Tests(TestCase):

    def test_engram(self):
        """
        Make sure that simple greetings return an expected result.
        """
        engram = Engram()
        response = engram.engram("hi")

        self.assertTrue("hello" in response.lower())

    def test_twitter_api(self):
        """
        Make sure that results from the twitter api can be used.
        """
        pass
