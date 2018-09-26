from chatterbot.conversation import Statement
from chatterbot.output import Microsoft
from tests.api_tests.test_microsoft import MicrosoftTestCase


class MicrosoftAdapterTests(MicrosoftTestCase):

    def setUp(self):
        super().setUp()

        self.adapter = Microsoft(
            direct_line_token_or_secret='xtFDtPemROU.cwA.Mcs.qiScdaSx87ffj2l7OjSITqJFoN-9Ado5AgwVeknac94',
            conversation_id='IEyJvnDULgn'
        )

    def test_process_response(self):
        statement = Statement('Hi! What is your name?')
        data = self.adapter.process_response(statement)
        self.assertEqual('Hi! What is your name?', data)
