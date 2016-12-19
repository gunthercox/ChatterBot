from __future__ import unicode_literals
from time import sleep
from chatterbot.input import InputAdapter
from chatterbot.conversation import Statement


class Microsoft(InputAdapter):
    """
    An input adapter that allows a ChatterBot instance to get
    input statements from a Microsoft Bot using *Directline client protocol*.
    https://docs.botframework.com/en-us/restapi/directline/#navtitle
    """

    def __init__(self, **kwargs):
        super(Microsoft, self).__init__(**kwargs)
        import requests
        from requests.packages.urllib3.exceptions import InsecureRequestWarning
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

        self.directline_host = kwargs.get('directline_host', 'https://directline.botframework.com')

        # NOTE: Direct Line client credentials are different from your bot's
        # credentials
        self.direct_line_token_or_secret = kwargs.\
            get('direct_line_token_or_secret')

        authorization_header = 'BotConnector  {}'.\
            format(self.direct_line_token_or_secret)

        self.headers = {
            'Authorization': authorization_header,
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'charset': 'utf-8'
        }

        conversation_data = self.start_conversation()
        self.conversation_id = conversation_data.get('conversationId')
        self.conversation_token = conversation_data.get('token')

    def _validate_status_code(self, response):
        code = response.status_code
        if not code == 200:
            raise self.HTTPStatusException('{} status code recieved'.
                                           format(code))

    def start_conversation(self):
        import requests

        endpoint = '{host}/api/conversations'.format(host=self.directline_host)
        response = requests.post(
            endpoint,
            headers=self.headers,
            verify=False
        )
        self.logger.info('{} starting conversation {}'.format(
            response.status_code, endpoint
        ))
        self._validate_status_code(response)
        return response.json()

    def get_most_recent_message(self):
        import requests

        endpoint = '{host}/api/conversations/{id}/messages'\
            .format(host=self.directline_host,
                    id=self.conversation_id)

        response = requests.get(
            endpoint,
            headers=self.headers,
            verify=False
        )

        self.logger.info('{} retrieving most recent messages {}'.format(
            response.status_code, endpoint
        ))

        self._validate_status_code(response)

        data = response.json()

        if data['messages']:
            last_msg = int(data['watermark'])
            return data['messages'][last_msg - 1]
        return None

    def process_input(self, statement):
        new_message = False
        data = None
        while not new_message:
            data = self.get_most_recent_message()
            if data and data['id']:
                new_message = True
            else:
                pass
            sleep(3.5)

        text = data['text']
        statement = Statement(text)
        self.logger.info('processing user statement {}'.format(statement))

        return statement

    class HTTPStatusException(Exception):
        """
        Exception raised when unexpected non-success HTTP
        status codes are returned in a response.
        """

        def __init__(self, value):
            self.value = value

        def __str__(self):
            return repr(self.value)
