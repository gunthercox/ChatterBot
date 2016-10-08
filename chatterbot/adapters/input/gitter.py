from chatterbot.adapters.input import InputAdapter
from chatterbot.conversation import Statement
from time import sleep
import requests
import json


class Gitter(InputAdapter):
    """
    An input adapter that allows a ChatterBot instance to get
    input statements from a Gitter room.
    """

    def __init__(self, **kwargs):
        super(Gitter, self).__init__(**kwargs)

        self.gitter_host = kwargs.get('gitter_host', 'https://api.gitter.im/v1/')
        self.gitter_room = kwargs.get('gitter_room')
        self.gitter_api_token = kwargs.get('gitter_api_token')

        authorization_header = 'Bearer {}'.format(self.gitter_api_token)

        self.headers = {
            'Authorization': authorization_header,
            'Content-Type': 'application/json',
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

    def mark_messages_as_read(self, message_ids):
        endpoint = '{}rooms/{}/unreadItems'.format(self.gitter_host, self.room_id)
        response = requests.post(
            endpoint,
            headers=self.headers,
            data=json.dumps({
                'chat': message_ids
            })
        )

    def get_most_recent_message(self):
        endpoint = '{}rooms/{}/chatMessages?limit=1'.format(self.gitter_host, self.room_id)
        response = requests.get(
            endpoint,
            headers=self.headers
        )
        data = response.json()
        if data:
            return data[0]
        return None

    def process_input(self, statement):
        new_message = False

        input_statement = self.context.get_last_input_statement()
        response_statement = self.context.get_last_response_statement()

        if input_statement:
            last_message_id = input_statement.extra_data.get(
                'gitter_message_id', None
            )
            if last_message_id:
                self.recent_message_ids.add(last_message_id)

        if response_statement:
            last_message_id = response_statement.extra_data.get(
                'gitter_message_id', None
            )
            if last_message_id:
                self.recent_message_ids.add(last_message_id)

        while not new_message:
            data = self.get_most_recent_message()

            if data and data['unread'] == True:
                self.mark_messages_as_read([data['id']])
                new_message = True
            sleep(3.5)

        statement = Statement(data['text'])

        return statement
