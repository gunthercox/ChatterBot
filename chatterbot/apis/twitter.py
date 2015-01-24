# -*- encoding: utf-8 -*-
from __future__ import unicode_literals
import requests
from requests_oauthlib import OAuth1


class Twitter(object):

    def __init__(self, twitter):

        self.REQUEST_TOKEN_URL = "https://api.twitter.com/oauth/request_token"
        self.AUTHORIZE_URL = "https://api.twitter.com/oauth/authorize?oauth_token="
        self.ACCESS_TOKEN_URL = "https://api.twitter.com/oauth/access_token"

        self.consumer_key = twitter["CONSUMER_KEY"]
        self.consumer_secret = twitter["CONSUMER_SECRET"]
        self.oauth_token = None
        self.oauth_token_secret = None

        # Resource owner variables used during authorization process
        self.resource_owner_key = None
        self.resource_owner_secret = None

        self.oauth = None

        # An exisitng oauth token can be passed in to skip this step.
        if "OAUTH_TOKEN" in twitter and "OAUTH_TOKEN_SECRET" in twitter:
            self.oauth_token = twitter["OAUTH_TOKEN"]
            self.oauth_token_secret = twitter["OAUTH_TOKEN_SECRET"]
            self.oauth = self.get_oauth()

    def get_authorization_url(self):
        from urlparse import parse_qs

        # Get request token
        oauth = OAuth1(self.consumer_key, client_secret=self.consumer_secret)
        response = requests.post(url=self.REQUEST_TOKEN_URL, auth=oauth)
        credentials = parse_qs(response.content)

        self.resource_owner_key = credentials.get("oauth_token")[0]
        self.resource_owner_secret = credentials.get("oauth_token_secret")[0]

        # Return the url to authorize request token
        return self.AUTHORIZE_URL + self.resource_owner_key

    def verify(self, verifier):
        from urlparse import parse_qs

        oauth = OAuth1(self.consumer_key,
                       client_secret=self.consumer_secret,
                       resource_owner_key=self.resource_owner_key,
                       resource_owner_secret=self.resource_owner_secret,
                       verifier=verifier)

        # Get the access token
        response = requests.post(url=self.ACCESS_TOKEN_URL, auth=oauth)
        credentials = parse_qs(response.content)

        self.oauth_token = credentials.get("oauth_token")[0]
        self.oauth_token_secret = credentials.get("oauth_token_secret")[0]
        self.oauth = self.get_oauth()

    def get_oauth(self):
        oauth = OAuth1(self.consumer_key,
                    client_secret=self.consumer_secret,
                    resource_owner_key=self.oauth_token,
                    resource_owner_secret=self.oauth_token_secret)
        return oauth

    def get_timeline(self):
        """
        Get status list
        """
        endpoint = "https://api.twitter.com/1.1/statuses/user_timeline.json"
        response = requests.get(url=timeline_endpoint, auth=self.oauth)

        return response.json()

    def post_update(self, message):
        # Post an update
        endpoint = "https://api.twitter.com/1.1/statuses/update.json"

        data = {
            "status": message
        }

        response = requests.post(url=endpoint, data=data, auth=self.oauth)

        return response.json()

    def favorite(self, tweet_id):
        endpoint = "https://api.twitter.com/1.1/favorites/create.json"

        data = {
            "id": tweet_id
        }

        response = requests.post(url=endpoint, data=data, auth=self.oauth)

        return response.json()

    def follow(self, username):
        endpoint = "https://api.twitter.com/1.1/friendships/create.json"

        data = {
            "follow": True,
            "screen_name": username
        }

        response = requests.post(url=endpoint, data=data, auth=self.oauth)

        return response.json()

    def get_list_users(self, username, slug):
        endpoint = "https://api.twitter.com/1.1/lists/members.json"
        endpoint += "?slug=" + slug + "&owner_screen_name=" + username

        response = requests.get(url=endpoint, auth=self.oauth)
        
        return list(str(user["screen_name"]) for user in response.json()["users"])

    def get_mentions(self):
        endpoint = "https://api.twitter.com/1.1/statuses/mentions_timeline.json"

        response = requests.get(url=endpoint, auth=self.oauth)

        return response.json()

    def search(self, q, count=1, result_type="mixed"):
        url = "https://api.twitter.com/1.1/search/tweets.json"
        url += "?q=" + q
        url += "&result_type=" + result_type
        url += "&count=" + str(count)

        response = requests.get(url=endpoint, auth=self.oauth)

        return response.json()

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

        response = requests.get(url=url, auth=self.oauth)

        return response.json()

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
