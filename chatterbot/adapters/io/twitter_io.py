# -*- encoding: utf-8 -*-
from chatterbot.adapters.io import IOAdapter
from chatterbot.conversation import Statement
import twitter
import threading
import time

try:
    from queue import Queue
except ImportError:
    # Use the python 2 queue import
    from Queue import Queue


class SimulatedAnnealingScheduler(object):
    """
    This class implements a simulated annealing algorithm to determine
    the correct schedule for running a function.
    The benefit of this class is that it is more efficient than interval
    checking when a given function may yield a greater probability of
    returning similar consecutive results.
    """

    def __init__(self, function, comparison_function, interval=5):
        """
        Takes a function to be run periodically and a comparison function to
        determine if the result of the function is true or false.
        """
        self.function = function
        self.check = comparison_function

        self.interval = interval

        # INTERVAL_MIN = 1 second
        self.INTERVAL_MIN = 1

        # INTERVAL_MAX = number of seconds in 1 day
        self.INTERVAL_MAX = 60 * 60 * 24

        self.INCREMENT_AMOUNT = 2
        self.DECREMENT_AMOUNT = 2

        self.thread = threading.Thread(target=self.start, args=())
        self.thread.daemon = True
        self.thread.start()

    def get_temperature(self, scaling_factor=10):
        pass

    def decrease_interval(self):
        """
        Decrement the interval as long as doing so will not cause it to
        decrease past the predefined minimum.
        """
        if (self.interval - self.DECREMENT_AMOUNT) >= self.INTERVAL_MIN:
            self.interval -= self.DECREMENT_AMOUNT

    def increase_interval(self):
        """
        Increment the interval as long as doing so will not cause it to
        increase past the predefined maximum.
        """
        if (self.interval + self.INCREMENT_AMOUNT) <= self.INTERVAL_MAX:
            self.interval += self.INCREMENT_AMOUNT

    def start(self):
        while True:
            result = self.function()

            if self.check(result):
                self.increase_interval()
            else:
                self.decrease_interval()

            time.sleep(self.interval)

    def stop(self):
        self.thread.stop()


class TwitterAdapter(IOAdapter):

    def __init__(self, **kwargs):
        super(TwitterAdapter, self).__init__(**kwargs)

        self.api = twitter.Api(
            consumer_key=kwargs["twitter_consumer_key"],
            consumer_secret=kwargs["twitter_consumer_secret"],
            access_token_key=kwargs["twitter_access_token_key"],
            access_token_secret=kwargs["twitter_access_token_secret"]
        )

        self.mention_queue = Queue()
        self.direct_message_queue = Queue()

        self.message_checker = SimulatedAnnealingScheduler(
            self.get_messages,
            self.is_new_message
        )

    def post_update(self, message):
        return self.api.PostUpdate(message)

    def favorite(self, tweet_id):
        return self.api.CreateFavorite(id=tweet_id)

    def follow(self, username):
        return self.api.CreateFriendship(screen_name=username)

    def get_list_users(self, username, slug):
        return self.api.GetListMembers(None, slug, owner_screen_name=username)

    def get_mentions(self):
        mentions = self.api.GetMentions()

        print "get_mentions:", mentions
        return mentions

    def is_new_message(self, data):
        print "message data:"
        for d in data:
            print "\t", d.text
            print "\t", d

        return True

    def get_messages(self):
        return self.api.GetDirectMessages(count=5)

    def search(self, q, count=1, result_type="mixed"):
        return self.api.GetSearch(term=q, count=count, result_type=result_type)

    def get_related_messages(self, text):
        results = search(text, count=50)
        replies = []
        non_replies = []

        for result in results["statuses"]:

            # Select only results that are replies
            if result["in_reply_to_status_id_str"] is not None:
                message = result["text"]
                replies.append(message)

            # Save a list of other results in case a reply cannot be found
            else:
                message = result["text"]
                non_replies.append(message)

        if len(replies) > 0:
            return replies

        return non_replies

    def reply(self, tweet_id, message):
        """
        Reply to a tweet
        """
        return self.api.PostUpdate(message, in_reply_to_status_id=tweet_id)

    def tweet_to_friends(self, username, slug, greetings, debug=False):
        """    
        Tweet one random message to the next friend in a list every hour.
        The tweet will not be sent and will be printed to the console when in
        debug mode.
        """
        from time import time, sleep
        from random import choice

        # Get the list of robots
        robots = self.get_list_users(username, slug=slug)

        for robot in robots:
            message = ("@" + robot + " " + choice(greetings)).strip("\n")

            if debug is True:
                print(message)
            else:
                sleep(3600-time() % 3600)
                t.statuses.update(status=message)

    def has_responeded_to_message(self, message_id):
        # TODO
        pass

    def process_input(self):
        """
        This method should check twitter for new mentions and
        return them as Statement objects.
        """
        # Download a list of recent mentions
        mentions = self.get_mentions()

        print "MENTIONS:", mentions

        for mention in mentions:
            mention = Statement(mention.text)

            # Add the mention to the mention queue if a response has not been made
            if not self.has_responeded_to_message(mention):
                self.mention_queue.put(mention)

    def process_response(self, input_statement):
        return input_statement

