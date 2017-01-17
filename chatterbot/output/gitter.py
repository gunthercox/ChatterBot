from __future__ import unicode_literals
from .output_adapter import OutputAdapter


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
        self.logger.info('{} status joining room {}'.format(
            response.status_code, endpoint
        ))
        self._validate_status_code(response)
        return response.json()

    def send_message(self, text):
        """
        Send a message to a Gitter room.
        """
        import requests

        endpoint = '{}rooms/{}/chatMessages'.format(self.gitter_host, self.room_id)
        response = requests.post(
            endpoint,
            headers=self.headers,
            json={'text': text}
        )
        self.logger.info('{} sending message to {}'.format(
            response.status_code, endpoint
        ))
        self._validate_status_code(response)
        return response.json()

    def process_response(self, statement, session_id=None):
        self.send_message(statement.text)
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
