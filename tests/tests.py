from unittest import TestCase
from ChatBot.engram import Engram


class Tests(TestCase):

    def test_engram(self):
        """
        Make sure that text is returned from an engram.
        """
        engram = Engram()
        response = engram.engram("hello")

        self.assertTrue(len(response) > 0)

    def test_twitter_api(self):
        """
        Make sure that results from the twitter api can be used.
        """
        pass
