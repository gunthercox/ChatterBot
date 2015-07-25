from unittest import TestCase
from chatterbot.adapters.io import TwitterAdapter


class TwitterTests(TestCase):

    def test_consumer_stored(self):
        TWITTER = {
            "CONSUMER_KEY": "blahblahblah",
            "CONSUMER_SECRET": "nullvoidnullvoidnullvoid"
        }

        chatbot = TwitterAdapter(twitter=TWITTER)

        self.assertEqual(TWITTER["CONSUMER_KEY"], chatbot.consumer_key)
        self.assertEqual(TWITTER["CONSUMER_SECRET"], chatbot.consumer_secret)

