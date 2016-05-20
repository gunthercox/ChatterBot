from chatterbot.adapters.output import OutputAdapter
import requests
import json


class HipChat(OutputAdapter):

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
        # https://www.hipchat.com/docs/apiv2/method/send_message

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
        # https://www.hipchat.com/docs/apiv2/method/reply_to_message
        pass

    def process_response(self, statement):
        data = self.send_message(self.hipchat_room, statement.text)

        # Update the output statement with the message id
        self.context.recent_statements[-1][1].add_extra_data(
            'hipchat_message_id', data['id']
        )

        return statement
