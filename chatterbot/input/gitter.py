from time import sleep
from chatterbot.input import InputAdapter
from chatterbot.api import gitter
from chatterbot.conversation import Statement


class Gitter(InputAdapter):
    """
    An input adapter that allows a ChatterBot instance to get
    input statements from a Gitter room.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.gitter_room = kwargs.get('gitter_room')
        self.gitter_api_token = kwargs.get('gitter_api_token')
        self.only_respond_to_mentions = kwargs.get('gitter_only_respond_to_mentions', True)
        self.sleep_time = kwargs.get('gitter_sleep_time', 4)

        # Join the Gitter room
        room_data = gitter.join_room(self.gitter_api_token, self.gitter_room)
        self.room_id = room_data.get('id')

        user_data = gitter.get_user_data(self.gitter_api_token)
        self.user_id = user_data[0].get('id')
        self.username = user_data[0].get('username')

    def process_input(self, statement):
        new_message = False

        while not new_message:
            data = gitter.get_most_recent_message(self.gitter_api_token, self.room_id)
            if gitter.should_respond(data, self.username, self.only_respond_to_mentions):
                gitter.mark_messages_as_read(
                    self.gitter_api_token,
                    self.user_id,
                    self.room_id,
                    [data['id']]
                )
                new_message = True
            sleep(self.sleep_time)

        text = gitter.remove_mentions(data['text'])

        return Statement(text)
