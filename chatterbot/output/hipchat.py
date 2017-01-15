from __future__ import unicode_literals
import json
from .output_adapter import OutputAdapter


class HipChat(OutputAdapter):
    """
    An output adapter that allows a ChatterBot instance to send
    responses to a HipChat room.
    """

    def __init__(self, **kwargs):
        super(HipChat, self).__init__(**kwargs)

        self.hipchat_host = kwargs.get("hipchat_host")
        self.hipchat_access_token = kwargs.get("hipchat_access_token")
        self.hipchat_room = kwargs.get("hipchat_room")

        authorization_header = "Bearer {}".format(self.hipchat_access_token)

        self.headers = {
            'Authorization': authorization_header,
            'Content-Type': 'application/json'
        }

    def send_message(self, room_id_or_name, message):
        """
        Send a message to a HipChat room.
        https://www.hipchat.com/docs/apiv2/method/send_message
        """
        import requests

        message_url = "{}/v2/room/{}/message".format(
            self.hipchat_host,
            room_id_or_name
        )

        response = requests.post(
            message_url,
            headers=self.headers,
            data=json.dumps({
                'message': message
            })
        )

        return response.json()

    def reply_to_message(self):
        """
        The HipChat api supports responding to a given message.
        This may be a good feature to implement in the future to
        help with multi-user conversations.
        https://www.hipchat.com/docs/apiv2/method/reply_to_message
        """
        raise self.AdapterMethodNotImplementedError()

    def process_response(self, statement, session_id=None):
        data = self.send_message(self.hipchat_room, statement.text)

        # Update the output statement with the message id
        self.chatbot.conversation_sessions.get(session_id).conversation[-1][1].add_extra_data(
            'hipchat_message_id', data['id']
        )

        return statement
