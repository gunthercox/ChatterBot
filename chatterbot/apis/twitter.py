class Twitter(object):
 
    def __init__(self, TWITTER):
        import oauth2 as oauth

        consumer = oauth.Consumer(key=TWITTER["CONSUMER_KEY"], secret=TWITTER["CONSUMER_SECRET"])
        access_token = oauth.Token(key=TWITTER["ACCESS_KEY"], secret=TWITTER["ACCESS_SECRET"])

        self.client = oauth.Client(consumer, access_token)

    def get_timeline(self):
        """
        Get status list
        """
        import json

        timeline_endpoint = "https://api.twitter.com/1.1/statuses/user_timeline.json"
        response, data = self.client.request(timeline_endpoint)

        return json.loads(data)

    def post_update(self, message):
        # Post an update
        url = "https://api.twitter.com/1.1/statuses/update.json"
        url += "?status=" + message.replace(" ", "%20")

        self.client.request(url, method="POST")

    def favorite(self, tweet_id):
        url = "https://api.twitter.com/1.1/favorites/create.json"
        url += "?id=" + str(tweet_id)

        self.client.request(url, method="POST")

    def follow(self, username):
        url = "https://api.twitter.com/1.1/friendships/create.json"
        url += "?follow=true&screen_name=" + username

        self.client.request(url, method="POST")

    def get_list_users(self, username, slug):
        import json

        url = "https://api.twitter.com/1.1/lists/members.json"
        url += "?slug=" + slug + "&owner_screen_name=" + username

        response, data = self.client.request(url)
        data = json.loads(data)
        
        return list(str(user["screen_name"]) for user in data["users"])

    def get_mentions(self):
        import json

        url = "https://api.twitter.com/1.1/statuses/mentions_timeline.json"

        response, data = self.client.request(url)
        data = json.loads(data)

        return data

    def search(self, q, count=1, result_type="mixed"):
        import json

        url = "https://api.twitter.com/1.1/search/tweets.json"
        url += "?q=" + q
        url += "&result_type=" + result_type
        url += "&count=" + str(count)

        response, data = self.client.request(url)
        data = json.loads(data)

        return data

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

    def get_activity_data(self):
        """
        Counts the activity frequency for each day of the week.
        """
        timeline = get_timeline() #count=500
        daily_sum = {
            "Sun": 0,
            "Mon": 0,
            "Tue": 0,
            "Wed": 0,
            "Thu": 0,
            "Fri": 0,
            "Sat": 0,
        }

        for post in timeline:
            day = post["created_at"].split(" ")[0]
            daily_sum[day] += 1

        return daily_sum

    def reply(self, tweet_id, message):
        """
        Reply to a tweet
        """
        url = "https://api.twitter.com/1.1/statuses/update.json"
        url += "?status=" + message.replace(" ", "%20")
        url += "&in_reply_to_status_id=" + str(tweet_id)

        self.client.request(url, method="POST")

    def tweet_to_friends(self, username, slug, greetings, debug=False):
        """    
        Tweet one random message to the next friend in a list every hour.
        The tweet will not be sent and will be printed to the console when in
        debug mode.
        """
        from time import time, sleep
        from random import choice

        # Get the list of robots
        robots =  get_list_users(username, slug=slug)

        for robot in robots:
            message = ("@" + robot + " " + choice(greetings)).strip("\n")

            if debug is True:
                print(message)
            else:
                sleep(3600-time() % 3600)
                t.statuses.update(status=message)
