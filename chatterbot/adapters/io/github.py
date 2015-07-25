from chatterbot.adapters.io import IOAdapter
import requests


class GitHubAdapter(IOAdapter):

    def __init__(self, github):
        self.github = github

    def get_authorization_url(self):
        # Generate a random string for the state parameter
        # Save it for use later to prevent xsrf attacks
        from uuid import uuid4
        import urllib

        state = str(uuid4())
        params = {
            "client_id": self.github["CLIENT_ID"],
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
