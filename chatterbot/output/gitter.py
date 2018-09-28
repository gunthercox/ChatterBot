from chatterbot.output import OutputAdapter
from chatterbot.api import gitter


class Gitter(OutputAdapter):
    """
    An output adapter that allows a ChatterBot instance to send
    responses to a Gitter room.
    """

    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)

        self.gitter_room = kwargs.get('gitter_room')
        self.gitter_api_token = kwargs.get('gitter_api_token')

        # Join the Gitter room
        room_data = gitter.join_room(self.gitter_api_token, self.gitter_room)
        self.room_id = room_data.get('id')

    def process_response(self, statement):
        gitter.send_message(self.gitter_api_token, self.room_id, statement.text)
        return statement
