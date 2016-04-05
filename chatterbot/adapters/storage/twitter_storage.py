from chatterbot.adapters.storage import StorageAdapter
from chatterbot.conversation import Statement, Response
import random
import twitter


class TwitterAdapter(StorageAdapter):
    """
    The TwitterAdapter allows ChatterBot to read tweets from twitter.
    """

    def __init__(self, **kwargs):
        super(TwitterAdapter, self).__init__(**kwargs)

        self.api = twitter.Api(
            consumer_key=kwargs.get('twitter_consumer_key'),
            consumer_secret=kwargs.get('twitter_consumer_secret'),
            access_token_key=kwargs.get('twitter_access_token_key'),
            access_token_secret=kwargs.get('twitter_access_token_secret')
        )

    def count(self):
        return 1

    def find(self, statement_text):
        tweets = self.api.GetSearch(term=statement_text, count=1)

        if tweets:
            return Statement(tweets[0].text, in_response_to=[
                Response(statement_text)
            ])

        return None

    def filter(self, **kwargs):
        """
        Returns a list of statements in the database
        that match the parameters specified.
        """
        statement_text = kwargs.get('text')

        # if not statement_text:
        #    statement_text = kwargs.get('in_response_to__contains')
        # data['in_reply_to_status_id_str']

        # If no text parameter was given get a selection of recent tweets
        if not statement_text:
            statements = self.get_random(number=20)
            return statements

        tweets = self.api.GetSearch(term=statement_text)
        tweet = random.choice(tweets)

        statement = Statement(tweet.text, in_response_to=[
            Response(statement_text)
        ])

        return [statement]

    def update(self, statement):
        return statement

    def choose_word(self, words):
        """
        Light weight search for a valid word if one exists.
        """
        for word in words:
            # If the word contains only letters with a length from 4 to 9
            if word.isalpha() and len(word) > 3 and len(word) <= 9:
                return word

        return None

    def get_random(self, number=1):
        """
        Returns a random statement from the api.
        To generate a random tweet, search twitter for recent tweets
        containing the term 'random'. Then randomly select one tweet
        from the current set of tweets. Randomly choose one word from
        the selected random tweet, and make a second search request.
        Return one random tweet selected from the search results.
        """
        statements = []
        tweets = self.api.GetSearch(term="random", count=5)

        tweet = random.choice(tweets)
        base_response = Response(text=tweet.text)

        words = tweet.text.split()
        word = self.choose_word(words)

        # If a valid word is found, make a second search request
        # TODO: What if a word is not found?
        if word:
            tweets = self.api.GetSearch(term=word, count=number)
            if tweets:
                for tweet in tweets:
                    # TODO: Handle non-ascii characters properly
                    cleaned_text = ''.join(
                        [i if ord(i) < 128 else ' ' for i in tweet.text]
                    )
                    statements.append(
                        Statement(cleaned_text, in_response_to=[base_response])
                    )

        if number == 1:
            return random.choice(statements)

        return statements

    def drop(self):
        """
        Twitter is only a simulated data source in
        this case so it cannot be removed.
        """
        pass
