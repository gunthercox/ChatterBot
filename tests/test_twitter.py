from unittest import TestCase
from chatterbot.apis.twitter import Twitter
from chatterbot.algorithms.twitter import remove_leeding_usernames
from chatterbot.algorithms.twitter import remove_trailing_usernames


class TwitterTests(TestCase):

    def test_consumer_stored(self):
        TWITTER = {
            "CONSUMER_KEY": "blahblahblah",
            "CONSUMER_SECRET": "nullvoidnullvoidnullvoid"
        }

        chatbot = Twitter(twitter=TWITTER)

        self.assertEqual(TWITTER["CONSUMER_KEY"], chatbot.consumer_key)
        self.assertEqual(TWITTER["CONSUMER_SECRET"], chatbot.consumer_secret)

