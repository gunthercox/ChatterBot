from __future__ import unicode_literals
from time import sleep
from chatterbot.input import InputAdapter
from chatterbot.conversation import Statement


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
        self.only_respond_to_mentions = kwargs.get('gitter_only_respond_to_mentions', True)
        self.sleep_time = kwargs.get('gitter_sleep_time', 4)

        authorization_header = 'Bearer {}'.format(self.gitter_api_token)

        self.headers = {
            'Authorization': authorization_header,
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

        # Join the Gitter room
        room_data = self.join_room(self.gitter_room)
        self.room_id = room_data.get('id')

        user_data = self.get_user_data()
        self.user_id = user_data[0].get('id')
        self.username = user_data[0].get('username')

    def _validate_status_code(self, response):
        code = response.status_code
        if code not in [200, 201]:
            raise self.HTTPStatusException('{} status code recieved'.format(code))

    def join_room(self, room_name):
        """
        Join the specified Gitter room.
        """
        import requests

        endpoint = '{}rooms'.format(self.gitter_host)
        response = requests.post(
            endpoint,
            headers=self.headers,
            json={'uri': room_name}
        )
        self.logger.info('{} joining room {}'.format(
            response.status_code, endpoint
        ))
        self._validate_status_code(response)
        return response.json()

    def get_user_data(self):
        import requests

        endpoint = '{}user'.format(self.gitter_host)
        response = requests.get(
            endpoint,
            headers=self.headers
        )
        self.logger.info('{} retrieving user data {}'.format(
            response.status_code, endpoint
        ))
        self._validate_status_code(response)
        return response.json()

    def mark_messages_as_read(self, message_ids):
        """
        Mark the specified message ids as read.
        """
        import requests

        endpoint = '{}user/{}/rooms/{}/unreadItems'.format(
            self.gitter_host, self.user_id, self.room_id
        )
        response = requests.post(
            endpoint,
            headers=self.headers,
            json={'chat': message_ids}
        )
        self.logger.info('{} marking messages as read {}'.format(
            response.status_code, endpoint
        ))
        self._validate_status_code(response)
        return response.json()

    def get_most_recent_message(self):
        """
        Get the most recent message from the Gitter room.
        """
        import requests

        endpoint = '{}rooms/{}/chatMessages?limit=1'.format(self.gitter_host, self.room_id)
        response = requests.get(
            endpoint,
            headers=self.headers
        )
        self.logger.info('{} getting most recent message'.format(
            response.status_code
        ))
        self._validate_status_code(response)
        data = response.json()
        if data:
            return data[0]
        return None

    def _contains_mention(self, mentions):
        for mention in mentions:
            if self.username == mention.get('screenName'):
                return True
        return False

    def should_respond(self, data):
        """
        Takes the API response data from a single message.
        Returns true if the chat bot should respond.
        """
        if data:
            unread = data.get('unread', False)

            if self.only_respond_to_mentions:
                if unread and self._contains_mention(data['mentions']):
                    return True
                else:
                    return False
            elif unread:
                return True

        return False

    def remove_mentions(self, text):
        """
        Return a string that has no leading mentions.
        """
        import re
        from chatterbot.utils import clean_whitespace
        text_without_mentions = re.sub(r'@\S+', '', text)
        return clean_whitespace(text_without_mentions)

    def process_input(self, statement):
        new_message = False

        while not new_message:
            data = self.get_most_recent_message()
            if self.should_respond(data):
                self.mark_messages_as_read([data['id']])
                new_message = True
            sleep(self.sleep_time)

        text = self.remove_mentions(data['text'])
        statement = Statement(text)

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
