from chatterbot.conversation import Statement
from chatterbot.output import Gitter
from tests.api_tests.test_gitter import GitterTestCase


class GitterAdapterTestCase(GitterTestCase):

    def setUp(self):
        super().setUp()

        self.adapter = Gitter(
            self.chatbot,
            gitter_room='',
            gitter_api_token='',
            gitter_sleep_time=0,
            gitter_only_respond_to_mentions=False
        )

    def test_process_response(self):
        statement = Statement('Hello')
        output_statement = self.adapter.process_response(statement)

        self.assertEqual(output_statement, statement)
