from tests.base_case import ChatBotTestCase
from chatterbot.logic import TimeLogicAdapter
from chatterbot.conversation import Statement


class TimeAdapterTests(ChatBotTestCase):

    def setUp(self):
        super().setUp()
        self.adapter = TimeLogicAdapter(self.chatbot)

    def test_positive_input(self):
        statement = Statement(text="Do you know what time it is?")
        response = self.adapter.process(statement)

        self.assertEqual(response.confidence, 1)
        self.assertIn("The current time is ", response.text)

    def test_negative_input(self):
        statement = Statement(text="What is an example of a pachyderm?")
        response = self.adapter.process(statement)

        self.assertEqual(response.confidence, 0)
        self.assertIn("The current time is ", response.text)
