from chatterbot.adapters.storage import DatabaseAdapter
from chatterbot.conversation import Statement
from application_only_auth import Client


class TwitterAdapter(DatabaseAdapter):

    def __init__(self, **kwargs):
        super(TwitterAdapter, self).__init__(**kwargs)

        CONSUMER_KEY = kwargs["consumer_key"]
        CONSUMER_SECRET = kwargs["consumer_secret"]

        self.client = Client(CONSUMER_KEY, CONSUMER_SECRET)

    def search(self, q, count=1, result_type="recent"):
        import urllib

        # Remove non-ascii characters from the search string
        cleaned = ''.join(
            [i if ord(i) < 128 else ' ' for i in q]
        )

        query = urllib.quote(cleaned)

        url = "https://api.twitter.com/1.1/search/tweets.json"
        url += "?q=" + query
        url += "&result_type=" + result_type
        url += "&count=" + str(count)

        return self.client.request(url)

    def count(self):
        return 1

    def find(self, statement_text):
        data = self.search(statement_text)

        for d in data['statuses']:
            print ">>", d['in_reply_to_status_id_str']

        result_text = data['statuses'][0]['text']

        return Statement(result_text)

    def filter(self, **kwargs):
        """
        Returns a list of statements in the database
        that match the parameters specified.
        """
        statement_text = kwargs.get('text')

        if not statement_text:
            statement_text = kwargs.get('in_response_to__contains')

        if not statement_text:
            # If no text parameter was given get a selection of recent tweets
            statements = []
            data = self.search('none', count=20)
            for item in data['statuses']:
                statements.append(
                    Statement(item['text'])
                )
            return statements

        data = self.search(statement_text)
        result_text = data['statuses'][0]['text']

        statement = Statement(result_text)

        return [statement]

    def update(self, statement):
        return statement

    def get_random(self):
        """
        Returns a random statement from the api.
        """
        #data = self.search("random")
        data = self.client.request('https://stream.twitter.com/1.1/statuses/sample.json')

        # TODO: Choose one of the statuses at random:

        options = ["electronic", "brains", "robot", "zombie", "party", "cool"]

        print "MULTULE:", data['statuses']

        statement_text = data['statuses'][0]['text']

        return Statement(statement_text)

    def drop(self):
        """
        Twitter is only a simulated data source in
        this case so it cannot be removed.
        """
        pass

