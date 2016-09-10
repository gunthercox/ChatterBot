from tests.base_case import ChatBotTestCase
from chatterbot.adapters.logic import SentimentAdapter
from chatterbot.conversation import Statement


class SentimentAdapterTests(ChatBotTestCase):

    def setUp(self):
        super(SentimentAdapterTests, self).setUp()
        self.adapter = SentimentAdapter()
        self.adapter.set_context(self.chatbot)

    def test_exact_input(self):

        self.chatbot.train([
            'What is your favorite flavor of ice cream?',
            'I love raspberry ice cream',
            'That is great',
            'Thank you'
        ])

        happy_statement = Statement('I love raspberry ice cream')
        confidence, response = self.adapter.process(happy_statement)

        self.assertEqual(confidence, 0.7)
        self.assertEqual(response.text, 'That is great')

    def test_close_input(self):

        self.chatbot.train([
            'I love ice cream',
            'That is great',
            'Thank you'
        ])

        happy_statement = Statement('I like ice cream')
        confidence, response = self.adapter.process(happy_statement)

        print response

        self.assertEqual(confidence, 0.2)
        self.assertEqual(response.text, 'That is great')
