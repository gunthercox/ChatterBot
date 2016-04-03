from unittest import TestCase
from unittest import SkipTest
from mock import Mock, MagicMock
from chatterbot.adapters.storage import TwitterAdapter
import os
import json

def side_effect(*args, **kwargs):
    from twitter import Status

    # A special case for testing a response with no results
    if 'term' in kwargs and kwargs.get('term') == 'Non-existant':
        return []

    current_directory = os.path.dirname(os.path.realpath(__file__))
    data_file = os.path.join(
        current_directory,
        'test_data',
        'get_search.json'
    )
    tweet_data = open(data_file)
    data = json.loads(tweet_data.read())
    tweet_data.close()

    return [Status.NewFromJsonDict(x) for x in data.get('statuses', '')]


class TwitterAdapterTestCase(TestCase):

    def setUp(self):
        """
        Instantiate the adapter.
        """
        self.adapter = TwitterAdapter(
            twitter_consumer_key='twitter_consumer_key',
            twitter_consumer_secret='twitter_consumer_secret',
            twitter_access_token_key='twitter_access_token_key',
            twitter_access_token_secret='twitter_access_token_secret'
        )
        self.adapter.api = Mock()

        self.adapter.api.GetSearch = MagicMock(side_effect=side_effect)

    def test_count(self):
        """
        The count should always be 1.
        """
        self.assertEqual(self.adapter.count(), 1)

    def test_count(self):
        """
        The update method should return the input statement.
        """
        from chatterbot.conversation import Statement
        statement = Statement('Hello')
        result = self.adapter.update(statement)
        self.assertEqual(statement, result)

    def test_choose_word(self):
        words = ['G', 'is', 'my', 'favorite', 'letter']
        word = self.adapter.choose_word(words)
        self.assertEqual(word, words[3])

    def test_choose_no_word(self):
        words = ['q']
        word = self.adapter.choose_word(words)
        self.assertEqual(word, None)

    def test_drop(self):
        """
        This drop method should do nothing.
        """
        self.adapter.drop()

    def test_get_tweets(self):
        statements = self.adapter.filter()
        self.assertEqual(len(statements), 20)

    def test_statement_not_found(self):
        """
        Test the case that a match is not found.
        """
        statement = self.adapter.find('Non-existant')
        self.assertEqual(statement, None)

    def test_statement_found(self):
        found_statement = self.adapter.find('New statement')
        self.assertNotEqual(found_statement, None)
        self.assertTrue(len(found_statement.text))

    def test_filter(self):
        statements = self.adapter.filter(
            text__contains='a few of my favorite things'
        )
        self.assertGreater(len(statements), 0)

    def test_get_random(self):
        statement = self.adapter.get_random()
        self.assertNotEqual(statement, None)
        self.assertTrue(len(statement.text))
