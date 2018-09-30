from chatterbot.conversation import Statement
from chatterbot.input import Microsoft
from tests.api_tests.test_microsoft import MicrosoftTestCase


class MicrosoftInputAdapterTests(MicrosoftTestCase):

    def setUp(self):
        super().setUp()

        self.adapter = Microsoft(
            self.chatbot,
            direct_line_token_or_secret='xtFDtPemROU.cwA.Mcs.qiScdaSx87ffj2l7OjSITqJFoN-9Ado5AgwVeknac94',
        )

    def test_process_input(self):
        statement = Statement(text='Hi! What is your name?')
        data = self.adapter.process_input(statement)
        self.assertEqual('Hi! What is your name?', data)
