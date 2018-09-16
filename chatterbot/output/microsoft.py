import json
from .output_adapter import OutputAdapter


class Microsoft(OutputAdapter):
    """
    An output adapter that allows a ChatterBot instance to send
    responses to a Microsoft bot using *Direct Line client protocol*.
    """

    def __init__(self, **kwargs):
        super(Microsoft, self).__init__(**kwargs)

        self.directline_host = kwargs.get(
            'directline_host',
            'https://directline.botframework.com'
        )
        self.direct_line_token_or_secret = kwargs.get(
            'direct_line_token_or_secret'
        )
        self.conversation_id = kwargs.get('conversation_id')

        authorization_header = 'BotConnector {}'.format(
            self.direct_line_token_or_secret
        )

        self.headers = {
            'Authorization': authorization_header,
            'Content-Type': 'application/json'
        }

    def _validate_status_code(self, response):
        status_code = response.status_code
        if status_code not in [200, 204]:
            raise self.HTTPStatusException('{} status code received'.format(status_code))

    def get_most_recent_message(self):
        """
        Return the most recently sent message.
        """
        import requests
        endpoint = '{host}/api/conversations/{id}/messages'.format(
            host=self.directline_host,
            id=self.conversation_id
        )

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

    def send_message(self, conversation_id, message):
        """
        Send a message to a HipChat room.
        https://www.hipchat.com/docs/apiv2/method/send_message
        """
        import requests

        message_url = "{host}/api/conversations/{conversationId}/messages".format(
            host=self.directline_host,
            conversationId=conversation_id
        )

        response = requests.post(
            message_url,
            headers=self.headers,
            data=json.dumps({
                'message': message
            })
        )

        self.logger.info('{} sending message {}'.format(
            response.status_code, message_url
        ))
        self._validate_status_code(response)
        # Microsoft return 204 on operation succeeded and no content was returned.
        return self.get_most_recent_message()

    def process_response(self, statement):
        data = self.send_message(self.conversation_id, statement.text)
        self.logger.info('processing user response {}'.format(data))
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
