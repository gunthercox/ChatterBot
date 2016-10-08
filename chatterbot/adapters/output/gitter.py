from chatterbot.adapters.output import OutputAdapter
import requests
import json


class Gitter(OutputAdapter):
    """
    An output adapter that allows a ChatterBot instance to send
    responses to a Gitter room.
    """

    def __init__(self, **kwargs):
        super(Gitter, self).__init__(**kwargs)

        self.gitter_host = kwargs.get('gitter_host', 'https://api.gitter.im/v1/')
        self.gitter_room = kwargs.get('gitter_room')
        self.gitter_api_token = kwargs.get('gitter_api_token')

        authorization_header = 'Bearer {}'.format(self.gitter_api_token)

        self.headers = {
            'Authorization': authorization_header,
            'Content-Type': 'application/json; charset=utf-8',
            'Accept': 'application/json'
        }

        # Join the Gitter room
        room_data = self.join_room(self.gitter_room)
        self.room_id = room_data.get('id')

    def join_room(self, room_name):
        endpoint = '{}rooms'.format(self.gitter_host)
        response = requests.post(
            endpoint,
            headers=self.headers,
            data=json.dumps({
                'uri': room_name
            })
        )
        return response.json()

    def send_message(self, text):
        """
        Send a message to a Gitter room.
        """
        endpoint = '{}rooms/{}/chatMessages'.format(self.gitter_host, self.room_id)
        response = requests.post(
            endpoint,
            headers=self.headers,
            data=json.dumps({
                'text': text
            })
        )

    def process_response(self, statement):
        self.send_message(statement.text)
        return statement
