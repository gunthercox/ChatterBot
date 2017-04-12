from __future__ import unicode_literals
from time import sleep
from chatterbot.input import InputAdapter
from chatterbot.conversation import Statement


class HipChat(InputAdapter):
    """
    An input adapter that allows a ChatterBot instance to get
    input statements from a HipChat room.
    """

    def __init__(self, **kwargs):
        super(HipChat, self).__init__(**kwargs)

        self.hipchat_host = kwargs.get('hipchat_host')
        self.hipchat_access_token = kwargs.get('hipchat_access_token')
        self.hipchat_room = kwargs.get('hipchat_room')
        self.session_id = str(self.chatbot.default_session.uuid)

        authorization_header = 'Bearer {}'.format(self.hipchat_access_token)

        self.headers = {
            'Authorization': authorization_header,
            'Content-Type': 'application/json'
        }

        # This is a list of the messages that have been responded to
        self.recent_message_ids = self.get_initial_ids()

    def get_initial_ids(self):
        """
        Returns a list of the most recent message ids.
        """
        data = self.view_recent_room_history(
            self.hipchat_room,
            max_results=75
        )

        results = set()

        for item in data['items']:
            results.add(item['id'])

        return results

    def view_recent_room_history(self, room_id_or_name, max_results=1):
        """
        https://www.hipchat.com/docs/apiv2/method/view_recent_room_history
        """
        import requests

        recent_histroy_url = '{}/v2/room/{}/history?max-results={}'.format(
            self.hipchat_host,
            room_id_or_name,
            max_results
        )

        response = requests.get(
            recent_histroy_url,
            headers=self.headers
        )

        return response.json()

    def get_most_recent_message(self, room_id_or_name):
        """
        Return the most recent message from the HipChat room.
        """
        data = self.view_recent_room_history(room_id_or_name)

        items = data['items']

        if not items:
            return None
        return items[-1]

    def process_input(self, statement):
        """
        Process input from the HipChat room.
        """
        new_message = False

        input_statement = self.chatbot.conversation_sessions.get(
            self.session_id).conversation.get_last_input_statement()
        response_statement = self.chatbot.conversation_sessions.get(
            self.session_id).conversation.get_last_response_statement()

        if input_statement:
            last_message_id = input_statement.extra_data.get(
                'hipchat_message_id', None
            )
            if last_message_id:
                self.recent_message_ids.add(last_message_id)

        if response_statement:
            last_message_id = response_statement.extra_data.get(
                'hipchat_message_id', None
            )
            if last_message_id:
                self.recent_message_ids.add(last_message_id)

        while not new_message:
            data = self.get_most_recent_message(self.hipchat_room)

            if data and data['id'] not in self.recent_message_ids:
                self.recent_message_ids.add(data['id'])
                new_message = True
            else:
                pass
            sleep(3.5)

        text = data['message']

        statement = Statement(text)
        statement.add_extra_data('hipchat_message_id', data['id'])

        return statement
