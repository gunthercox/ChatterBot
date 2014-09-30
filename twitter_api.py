import json
import logging
from httplib import HTTPException

import urllib

# For supporting puthon 2 and 3 urllib
try:
    from urllib2 import Request, HTTPError, URLError, urlopen
except ImportError:
    from urllib.request import urlopen
    from urllib.request import Request, HTTPError, URLError


API_VERSION = '1.1'
API_ENDPOINT = 'https://api.twitter.com'
REQUEST_TOKEN_URL = '%s/oauth2/token' % API_ENDPOINT
REQUEST_FAVORITE_LIST = '%s/%s/favorites/list.json' % (API_ENDPOINT, API_VERSION)
REQUEST_TWEET_LIST = '%s/%s/statuses/user_timeline.json' % (API_ENDPOINT, API_VERSION)
REQUEST_SEARCH = '%s/%s/search/tweets.json' % (API_ENDPOINT, API_VERSION)
REQUEST_LIST = '%s/%s/lists/members.json' % (API_ENDPOINT, API_VERSION)
CREATE_FAVORITE = '%s/%s/favorites/create.json' % (API_ENDPOINT, API_VERSION)


class TwitterAPI(object):
 
    def __init__(self, api_key, api_secret, token=None):
        self._api_key = api_key
        self._api_secret = api_secret
 
        if token:
            self._token = token
        else:
            self._token = self.connect()
 
        logging.info('Connected to twitter')
 
    def connect(self):
        """
        connect to twiter api end-point https://api.twitter.com/oauth2/token
        and obtain an oauth token
        """
        import base64

        bearer_token = '%s:%s' % (self._api_key, self._api_secret)
        encoded_bearer_token = base64.b64encode(bearer_token.encode('ascii'))
        request = Request(REQUEST_TOKEN_URL)
        request.add_header('Content-Type', 'application/x-www-form-urlencoded;charset=UTF-8')
        request.add_header('Authorization', 'Basic %s' % encoded_bearer_token.decode('utf-8'))
        request.add_data('grant_type=client_credentials'.encode('ascii'))
 
        try:
            response = urlopen(request)
        except HTTPError as e:
            logging.error('HTTPError = ' + str(e.code))
        except URLError as e:
            logging.error('URLError = ' + str(e.reason))
        except HTTPException as e:
            logging.error('HTTPException')
        except Exception:
            import traceback
            logging.error('generic exception: ' + traceback.format_exc())
 
        raw_data = response.read().decode('utf-8')
        data = json.loads(raw_data)
        return data['access_token']
 
    def _execute(self, url, params):
        params_encode = urllib.urlencode(params)
        full_url = "%s?%s" % (url, params_encode)

        print(full_url)
 
        request = Request(full_url)
        request.add_header('Authorization', 'Bearer %s' % self._token)
        try:
            response = urlopen(request)
        except HTTPError as e:
            logging.error('HTTPError = ' + str(e.code))
        except URLError as e:
            logging.error('URLError = ' + str(e.reason))
        except HTTPException as e:
            logging.error('HTTPException')
        except Exception:
            import traceback
            logging.error('generic exception: ' + traceback.format_exc())
        raw_data = response.read().decode('utf-8')
        data = json.loads(raw_data)
        return data

    def get_favourites(self, screen_name, count=20):
        params = {'count': count, 'screen_name':screen_name}
        data = self._execute(REQUEST_FAVORITE_LIST, params)
        return data
 
    def get_tweets(self, screen_name):
        params = {'screen_name':screen_name}
        data = self._execute(REQUEST_TWEET_LIST, params)
        return data

    def get_list(self, username, slug):
        params = {'owner_screen_name':username, 'slug':slug}
        data = self._execute(REQUEST_LIST, params)
        return data

    def get_mentions(self, username):
        """
        Search for the latest tweets about someone
        """
        mentions = []
        results = self.search(username, 25, "recent")

        print(results)

        for result in results["statuses"]:
            user = result["user"]["screen_name"]
            # Make sure someone else posted the status
            if user.lower() != username.lower():
                mentions.append(result)

        return mentions

    def search(self, q, count=1, result_type="mixed"):
        params = {'q':q, 'result_type':result_type, 'count':str(count)}
        data = self._execute(REQUEST_SEARCH, params)
        return data

    def favorite(self, tweet):
        """
        Favorites a tweet
        https://api.twitter.com/1/favorites/create/:id

        Does not work yet
        """
        import json
        data = json.dumps({"id": tweet["id_str"]}).encode()

        '''
        params = {
            'OAuth oauth_consumer_key': "GPeLKWfhARC4c3ad9fkBXwYBg",
            'oauth_nonce': "",
            'oauth_signature': "",
            'oauth_signature_method': "HMAC-SHA1",
            'oauth_timestamp': "1410127599",
            'oauth_token': "", #self._token
            'oauth_version': "1.0"
        }
        params_encode = urllib.urlencode(params)
        '''

        # https://dev.twitter.com/discussions/9068
        # https://dev.twitter.com/apps/5886583/oauth?nid=10607
        # https://dev.twitter.com/docs/auth/creating-signature

        request = Request(CREATE_FAVORITE, data)
        request.add_header('Authorization', 'Bearer %s' % self._token)
        request.add_header('Content-Type', 'application/x-www-form-urlencoded')

        #request.add_header('Authorization', json.dumps(params))

        try:
            response = urlopen(request)
            result = response.read()
            response.close()
        except HTTPError as error:
            print(">>>>>", error)

        #try:
        #print("Favorited: %s, %s" % (result['text'], result['id']))
        return result
        #except TwitterHTTPError as e:
        #    print("Error: ", e)
        #    return None

    def tweet_to_friends(self, username, slug, debug=False):
        """    
        Tweet one random message to the next friend in a list every hour.
        The tweet will not be sent and will be printed to the console when in
        debug mode.
        """
        from time import time, sleep
        from random import choice

        greetings = [
            "Hows it going?",
            "Good day to you.",
            "How are you doing?",
            "Greetings fellow robot.",
            "base64.b64decode('aGVsbG8=')",
            "0110100001100101011011000110110001101111"
        ]

        # Get the list of robots
        robots = self.get_list(username, slug="Robots")["users"]

        for robot in robots:
            message = ("@" + robot["screen_name"] + " " + choice(greetings)).strip("\n")

            if debug is True:
                print(message)
            else:
                sleep(3600-time() % 3600)
                t.statuses.update(status=message)

    def clean(self, text):
        import re, json

        # Remove links from message
        text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)

        # Replace linebreaks with spaces
        text = text.replace("\n", " ").replace("\r", " ")

        # Remove any leeding or trailing whitespace
        text = text.strip()

        # Remove non-ascii characters
        text = text.encode("ascii",errors="ignore")

        # Replace quotes
        text = text.replace("\"", "'")

        # Replace html characters with ascii equivilant
        text = text.replace("&amp;", "&")
        text = text.replace("&gt;", ">")
        text = text.replace("&lt;", "<")

        # Remove leeding usernames
        if (len(text) > 0) and (len(text.split(" ",1)) > 0) and (text[0] == "@"):
            text = text.split(" ",1)[1]
            text = self.clean(text)

        # Remove trailing usernames
        if (len(list(text.split(" ")[-1])) > 0) and (list(text.split(" ")[-1])[0] == "@"):
            text = text.rsplit(" ", 1)[0]

        return text

    def get_related_messages(self, text):
        results = self.search(text, 50)
        replies = []
        non_replies = []

        for result in results["statuses"]:

            # Select only results that are replies
            if result["in_reply_to_status_id_str"] is not None:
                message = self.clean(result["text"])
                replies.append(message)

            # Save a list of other results in case a reply cannot be found
            else:
                message = self.clean(result["text"])
                non_replies.append(message)

        if len(replies) == 0:
            return non_replies

        return replies
