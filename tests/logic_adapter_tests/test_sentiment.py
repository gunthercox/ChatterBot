from tests.base_case import ChatBotTestCase
from chatterbot.logic import SentimentAdapter
from chatterbot.conversation import Statement


class SentimentAdapterTests(ChatBotTestCase):

    def setUp(self):
        super(SentimentAdapterTests, self).setUp()
        from chatterbot.trainers import ListTrainer

        self.chatbot.set_trainer(ListTrainer)
        self.adapter = SentimentAdapter()
        self.adapter.set_chatbot(self.chatbot)

    def test_exact_input(self):

        self.chatbot.train([
            'What is your favorite flavor of ice cream?',
            'I enjoy raspberry ice cream.',
            'I am glad to hear that.',
            'Thank you.'
        ])

        happy_statement = Statement('I enjoy raspberry ice cream.')
        confidence, response = self.adapter.process(happy_statement)

        self.assertEqual(confidence, 1)
        self.assertEqual(response.text, 'I am glad to hear that.')

    def test_close_input(self):

        self.chatbot.train([
            'What is your favorite flavor of ice cream?',
            'I enjoy raspberry ice cream.',
            'I am glad to hear that.',
            'Thank you.'
        ])

        happy_statement = Statement('I like raspberry ice cream.')
        confidence, response = self.adapter.process(happy_statement)

        self.assertEqual(confidence, 0.6)
        self.assertEqual(response.text, 'I am glad to hear that.')
