from chatterbot.conversation import Statement
from chatterbot.input import Gitter
from tests.api.test_gitter import GitterTestCase


class GitterAdapterTests(GitterTestCase):

    def setUp(self):
        super().setUp()

        self.adapter = Gitter(
            self.chatbot,
            gitter_room='',
            gitter_api_token='',
            gitter_sleep_time=0,
            gitter_only_respond_to_mentions=False
        )

    def test_process_input(self):
        statement = Statement(text='Hello')
        data = self.adapter.process_input(statement)
        self.assertEqual('Hello', data)
