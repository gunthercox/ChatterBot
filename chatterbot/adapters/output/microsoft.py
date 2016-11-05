from chatterbot.adapters.output import OutputAdapter
import requests
import json


class Microsoft(OutputAdapter):
    """
    An output adapter that allows a ChatterBot instance to send
    responses to a Micorsoft bot using *Direct Line client protocol*.
    """

    def __init__(self, **kwargs):
        super(Microsoft, self).__init__(**kwargs)

        self.directline_host = kwargs.get("directline_host")
        self.direct_line_token_or_secret = kwargs.get("direct_line_token_or_secret")
        self.conversation_id = kwargs.get("conversation_id")

        authorization_header = 'BotConnector {}'.format(self.direct_line_token_or_secret)

        self.headers = {
            'Authorization': authorization_header,
            'Content-Type': 'application/json'
        }

    def get_most_recent_message(self, watermark='1'):
        endpoint = '{host}/api/conversations/{id}/messages?watermark={watermark}'\
            .format(host=self.directline_host,
                    id=self.conversation_id,
                    watermark=watermark)

        response = requests.get(
            endpoint,
            headers=self.headers
        )
        self.logger.info(u'{} getting most recent message'.format(
            response.status_code
        ))
        self._validate_status_code(response)
        data = response.json()
        if data["messages"]:
            return data["messages"][0]
        return None

    def send_message(self, conversation_id, message):
        """
        Send a message to a HipChat room.
        https://www.hipchat.com/docs/apiv2/method/send_message
        """

        message_url = "{host}/api/conversations/{conversationId}/messages".\
            format(host=self.directline_host, conversationId=conversation_id)

        response = requests.post(
            message_url,
            headers=self.headers,
            data=json.dumps({
                'message': message
            })
        )

        # Microsoft return 204 on operation succeeded and no content was returned.
        return self.get_most_recent_message()

    def process_response(self, statement, confidence=None):
        data = self.send_message(self.conversation_id, statement.text)
        # Update the output statement with the message id
        self.context.recent_statements[-1][1].add_extra_data(
            'microsoft_msg_id', data['id']
        )

        return statement
