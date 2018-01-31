from tests.base_case import ChatBotTestCase
from mock import Mock, MagicMock
from chatterbot.trainers import TwitterTrainer
import os
import json


def get_search_side_effect(*args, **kwargs):
    from twitter import Status

    current_directory = os.path.dirname(os.path.realpath(__file__))
    data_file = os.path.join(
        current_directory,
        'test_data',
        'get_search.json'
    )
    tweet_data = open(data_file)
    data = json.loads(tweet_data.read())
    tweet_data.close()

    return [Status.NewFromJsonDict(x) for x in data.get('statuses')]


def get_status_side_effect(*args, **kwargs):
    from twitter import Status

    current_directory = os.path.dirname(os.path.realpath(__file__))
    data_file = os.path.join(
        current_directory,
        'test_data',
        'get_search.json'
    )
    tweet_data = open(data_file)
    data = json.loads(tweet_data.read())
    tweet_data.close()

    return Status.NewFromJsonDict(data.get('statuses')[1])


class TwitterTrainerTestCase(ChatBotTestCase):

    def setUp(self):
        """
        Instantiate the trainer class for testing.
        """
        super(TwitterTrainerTestCase, self).setUp()

        self.trainer = TwitterTrainer(
            self.chatbot.storage,
            twitter_consumer_key='twitter_consumer_key',
            twitter_consumer_secret='twitter_consumer_secret',
            twitter_access_token_key='twitter_access_token_key',
            twitter_access_token_secret='twitter_access_token_secret',
            show_training_progress=False
        )
        self.trainer.api = Mock()

        self.trainer.api.GetSearch = MagicMock(side_effect=get_search_side_effect)
        self.trainer.api.GetStatus = MagicMock(side_effect=get_status_side_effect)

    def test_random_word(self):
        word = self.trainer.random_word('random')

        self.assertTrue(len(word) > 3)

    def test_get_words_from_tweets(self):
        tweets = get_search_side_effect()
        words = self.trainer.get_words_from_tweets(tweets)

        self.assertIn('about', words)
        self.assertIn('favorite', words)
        self.assertIn('things', words)

    def test_get_statements(self):
        statements = self.trainer.get_statements()

        self.assertEqual(len(statements), 1)

    def test_train(self):
        self.trainer.train()

        statement_created = self.trainer.storage.filter()
        self.assertTrue(len(statement_created))
