from tests.base_case import ChatBotMongoTestCase


class RepetitiveResponseFilterTestCase(ChatBotMongoTestCase):
    """
    Test case for the RepetitiveResponseFilter class.
    """

    def test_filter_selection(self):
        """
        Test that repetitive responses are filtered out of the results.
        """
        from chatterbot.filters import RepetitiveResponseFilter
        from chatterbot.trainers import ListTrainer

        self.chatbot.filters = (RepetitiveResponseFilter(), )
        self.chatbot.set_trainer(ListTrainer, **self.get_kwargs())

        self.chatbot.train([
            'Hi',
            'Hello',
            'Hi',
            'Hello',
            'Hi',
            'Hello',
            'How are you?',
            'I am good.',
            'Glad to hear',
            'How are you?'
        ])

        first_response = self.chatbot.get_response('Hello', conversation='training')
        second_response = self.chatbot.get_response('Hello', conversation='training')

        self.assertEqual('I am good.', first_response.text)
        self.assertEqual('Hi', second_response.text)
