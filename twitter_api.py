import urllib
import json
import urllib2
import httplib
import logging
from urllib2 import Request, urlopen


API_VERSION = '1.1'
API_ENDPOINT = 'https://api.twitter.com'
REQUEST_TOKEN_URL = '%s/oauth2/token' % API_ENDPOINT
REQUEST_FAVORITE_LIST = '%s/%s/favorites/list.json' % (API_ENDPOINT, API_VERSION)
REQUEST_TWEET_LIST = '%s/%s/statuses/user_timeline.json' % (API_ENDPOINT, API_VERSION)
REQUEST_SEARCH = '%s/%s/search/tweets.json' % (API_ENDPOINT, API_VERSION)

 
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
        '''
        connect to twiter api end-point https://api.twitter.com/oauth2/token
        and obtain an oauth token
        '''
        import base64

        bearer_token = '%s:%s' % (self._api_key, self._api_secret)
        encoded_bearer_token = base64.b64encode(bearer_token.encode('ascii'))
        request = Request(REQUEST_TOKEN_URL)
        request.add_header('Content-Type', 'application/x-www-form-urlencoded;charset=UTF-8')
        request.add_header('Authorization', 'Basic %s' % encoded_bearer_token.decode('utf-8'))
        request.add_data('grant_type=client_credentials'.encode('ascii'))
 
        try:
            response = urlopen(request)
        except urllib2.HTTPError, e:
            logging.error('HTTPError = ' + str(e.code))
        except urllib2.URLError, e:
            logging.error('URLError = ' + str(e.reason))
        except httplib.HTTPException, e:
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
 
        request = Request(full_url)
        request.add_header('Authorization', 'Bearer %s' % self._token)
        try:
            response = urlopen(request)
        except urllib2.HTTPError, e:
            logging.error('HTTPError = ' + str(e.code))
        except urllib2.URLError, e:
            logging.error('URLError = ' + str(e.reason))
        except httplib.HTTPException, e:
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

    def get_mentions(self, username):
        """
        Search for the latest tweets about someone
        """
        mentions = []
        results = self.search(username, 25, "recent")

        print results

        for result in results["statuses"]:
            user = result["user"]["screen_name"]
            # Make sure someone else posted the status
            if user.lower() != username.lower():
                mentions.append(result)

        return mentions

    def search(self, q, count, result_type="mixed"):
        params = {'q':q, 'result_type':result_type, 'count':str(count)}
        data = self._execute(REQUEST_SEARCH, params)
        return data

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
