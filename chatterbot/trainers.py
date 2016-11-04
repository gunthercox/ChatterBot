from .conversation import Statement, Response
from .corpus import Corpus
import logging


class Trainer(object):

    def __init__(self, storage, **kwargs):
        self.storage = storage
        self.corpus = Corpus()
        self.logger = logging.getLogger(__name__)

    def train(self, *args, **kwargs):
        raise self.TrainerInitializationException()

    class TrainerInitializationException(Exception):

        def __init__(self, value=None):
            default = (
                'A training class must specified before calling train(). ' +
                'See http://chatterbot.readthedocs.io/en/stable/training.html'
            )
            self.value = value or default

        def __str__(self):
            return repr(self.value)

    def _generate_export_data(self):
        result = []

        for statement in self.storage.filter():
            for response in statement.in_response_to:
                result.append([response.text, statement.text])

        return result

    def export_for_training(self, file_path='./export.json'):
        """
        Create a file from the database that can be used to
        train other chat bots.
        """
        from jsondb.db import Database
        database = Database(file_path)
        export = {'export': self._generate_export_data()}
        database.data(dictionary=export)


class ListTrainer(Trainer):

    def get_or_create(self, statement_text):
        """
        Return a statement if it exists.
        Create and return the statement if it does not exist.
        """
        statement = self.storage.find(statement_text)

        if not statement:
            statement = Statement(statement_text)

        return statement

    def train(self, conversation):
        statement_history = []

        for text in conversation:
            statement = self.get_or_create(text)

            if statement_history:
                statement.add_response(
                    Response(statement_history[-1].text)
                )

            statement_history.append(statement)
            self.storage.update(statement, force=True)


class ChatterBotCorpusTrainer(Trainer):

    def train(self, *corpora):
        trainer = ListTrainer(self.storage)

        for corpus in corpora:
            corpus_data = self.corpus.load_corpus(corpus)
            for data in corpus_data:
                for pair in data:
                    trainer.train(pair)


class TwitterTrainer(Trainer):

    def __init__(self, storage, **kwargs):
        super(TwitterTrainer, self).__init__(storage, **kwargs)
        from twitter import Api as TwitterApi

        self.api = TwitterApi(
            consumer_key=kwargs.get('twitter_consumer_key'),
            consumer_secret=kwargs.get('twitter_consumer_secret'),
            access_token_key=kwargs.get('twitter_access_token_key'),
            access_token_secret=kwargs.get('twitter_access_token_secret')
        )

    def random_word(self, base_word='random'):
        """
        Generate a random word using the Twitter API.

        Search twitter for recent tweets containing the term 'random'.
        Then randomly select one word from those tweets and do another
        search with that word. Return a randomly selected word from the
        new set of results.
        """
        import random
        random_tweets = self.api.GetSearch(term=base_word, count=5)
        random_words = self.get_words_from_tweets(random_tweets)
        random_word = random.choice(list(random_words))
        tweets = self.api.GetSearch(term=random_word, count=5)
        words = self.get_words_from_tweets(tweets)
        word = random.choice(list(words))
        return word

    def get_words_from_tweets(self, tweets):
        """
        Given a list of tweets, return the set of
        words from the tweets.
        """
        words = set()

        for tweet in tweets:
            # TODO: Handle non-ascii characters properly
            cleaned_text = ''.join(
                [i if ord(i) < 128 else ' ' for i in tweet.text]
            )
            tweet_words = cleaned_text.split()

            for word in tweet_words:
                # If the word contains only letters with a length from 4 to 9
                if word.isalpha() and len(word) > 3 and len(word) <= 9:
                    words.add(word)

        return words

    def get_statements(self):
        """
        Returns list of random statements from the API.
        """
        from twitter import TwitterError
        statements = []

        # Generate a random word
        random_word = self.random_word()

        self.logger.info(u'Requesting 50 random tweets containing the word {}'.format(random_word))
        tweets = self.api.GetSearch(term=random_word, count=50)
        for tweet in tweets:
            statement = Statement(tweet.text)

            if tweet.in_reply_to_status_id:
                try:
                    status = self.api.GetStatus(tweet.in_reply_to_status_id)
                    statement.add_response(Response(status.text))
                    statements.append(statement)
                except TwitterError as e:
                    self.logger.warning(str(e))

        self.logger.info('Adding {} tweets with responses'.format(len(statements)))

        return statements

    def train(self):
        for i in range(0, 10):
            statements = self.get_statements()
            for statement in statements:
                self.storage.update(statement, force=True)
