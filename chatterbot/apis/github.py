import requests

class GitHub(object):

    def __init__(self):
        from jsondb.db import Database

        self.db = Database("settings.db")
        self.token_key = "github_token"
        self.authorize_url = None

    def make_authorization_url(self, github):
        # Generate a random string for the state parameter
        # Save it for use later to prevent xsrf attacks
        from uuid import uuid4
        import urllib

        state = str(uuid4())
        params = {
            "client_id": github["CLIENT_ID"],
            "scope": "repo, user",
            "state": state
        }
        url = "https://github.com/login/oauth/authorize?"
        url += urllib.urlencode(params)
        return url

    def star_repo(self, repo_url):
        """
        PUT /user/starred/:owner/:repo
        """
        token = self.db.data(key=self.token_key)

        headers = {
            "Authorization": "token %s" % token,
            "Accept": "application/vnd.github.v3+json",
            "Content-Type": "application/json",
            "Content-Length": 0
        }

        response = requests.put(repo_url, headers=headers)

    def follow_user(self, user_url):
        """
        PUT /user/following/:username
        """
        token = self.db.data(key=self.token_key)

        headers = {
            "Authorization": "token %s" % token,
            "Accept": "application/vnd.github.v3+json",
            "Content-Type": "application/json",
            "Content-Length": 0
        }

        response = requests.put(repo_url, headers=headers)
