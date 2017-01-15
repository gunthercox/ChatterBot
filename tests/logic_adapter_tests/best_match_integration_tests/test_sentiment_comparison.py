from tests.base_case import ChatBotTestCase
from chatterbot.logic import BestMatch
from chatterbot.conversation import Statement


class BestMatchSentimentComparisonTestCase(ChatBotTestCase):
    """
    Integration tests for the BestMatch logic adapter
    using the similarity of sentiment polarity as a comparison function.
    """

    def setUp(self):
        super(BestMatchSentimentComparisonTestCase, self).setUp()
        from chatterbot.trainers import ListTrainer
        from chatterbot.comparisons import sentiment_comparison

        self.chatbot.set_trainer(ListTrainer)
        self.adapter = BestMatch(
            statement_comparison_function=sentiment_comparison
        )
        self.adapter.set_chatbot(self.chatbot)

    def test_exact_input(self):
        self.chatbot.train([
            'What is your favorite flavor of ice cream?',
            'I enjoy raspberry ice cream.',
            'I am glad to hear that.',
            'Thank you.'
        ])

        happy_statement = Statement('I enjoy raspberry ice cream.')
        response = self.adapter.process(happy_statement)

        self.assertEqual(response.confidence, 1)
        self.assertEqual(response.text, 'I am glad to hear that.')

    def test_close_input(self):

        self.chatbot.train([
            'What is your favorite flavor of ice cream?',
            'I enjoy raspberry ice cream.',
            'I am glad to hear that.',
            'Thank you.'
        ])

        happy_statement = Statement('I enjoy raspberry.')
        response = self.adapter.process(happy_statement)

        self.assertEqual(response.text, 'I am glad to hear that.')
        self.assertAlmostEqual(response.confidence, 0.75, places=1)
