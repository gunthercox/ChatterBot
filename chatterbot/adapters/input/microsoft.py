from chatterbot.adapters.input import InputAdapter
from chatterbot.conversation import Statement
from time import sleep
import requests


class Microsoft(InputAdapter):
    """
    An input adapter that allows a ChatterBot instance to get
    input statements from a Microsoft Bot using *Directline client protocol*.
    https://docs.botframework.com/en-us/restapi/directline/#navtitle
    """

    def __init__(self, **kwargs):
        super(Microsoft, self).__init__(**kwargs)

        self.directline_host = kwargs.get('directline_host',
                                      'https://directline.botframework.com')

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
        # This is a list of the messages that have been responded to
        self.recent_message_ids = self.get_initial_ids()

    def _validate_status_code(self, response):
        code = response.status_code
        if not code == 200:
            raise self.HTTPStatusException('{} status code recieved'.
                                           format(code))

    def get_initial_ids(self):
        """
        Returns a list of the most recent message ids.
        """
        data = self.get_most_recent_message(watermark='75')

        results = set()

        for message in data['messages']:
            results.add(message['id'])

        return results

    def start_conversation(self):
        endpoint = '{host}/api/conversations'.format(host=self.directline_host)
        response = requests.post(
            endpoint,
            headers=self.headers,
        )
        self.logger.info(u'{} starting conversation {}'.format(
            response.status_code, endpoint
        ))
        self._validate_status_code(response)
        return response.json()

    def get_most_recent_message(self, watermark='1'):
        endpoint = '{host}/api/conversations/{id}/messages?watermark={watermark}'\
            .format(host=self.directline_host,
                    id=self.conversation_id,
                    watermark=watermark)

        response = requests.get(
            endpoint,
            headers=self.hdeaders
        )
        self.logger.info(u'{} getting most recent message'.format(
            response.status_code
        ))
        self._validate_status_code(response)
        data = response.json()
        if data["messages"]:
            return data["messages"][0]
        return None

    def process_input(self, statement):
        new_message = False

        input_statement = self.context.get_last_input_statement()
        response_statement = self.context.get_last_response_statement()

        if input_statement:
            last_message_id = input_statement.extra_data.get('microsoft_msg_id',
                                                             None)
            if last_message_id:
                self.recent_message_ids.add(last_message_id)

        if response_statement:
            last_message_id = response_statement.extra_data.\
                get('microsoft_msg_id', None)
            if last_message_id:
                self.recent_message_ids.add(last_message_id)

        while not new_message:
            data = self.get_most_recent_message()

            if data and data['id'] not in self.recent_message_ids:
                self.recent_message_ids.add(data['id'])
                new_message = True
            else:
                pass
            sleep(3.5)

        text = data['text']

        statement = Statement(text)
        statement.add_extra_data('microsoft_msg_id', data['id'])

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

