from tests.base_case import ChatBotMongoTestCase
from chatterbot import filters


class RepetitiveResponseFilterTestCase(ChatBotMongoTestCase):
    """
    Test case for the repetitive response filter.
    """

    def test_filter_selection(self):
        """
        Test that repetitive responses are filtered out of the results.
        """
        from chatterbot.conversation import Statement
        from chatterbot.trainers import ListTrainer

        self.chatbot.filters = (filters.get_recent_repeated_responses, )

        self.trainer = ListTrainer(
            self.chatbot,
            show_training_progress=False
        )

        self.trainer.train([
            'Hi',
            'Hello',
            'Hi',
            'Hello',
            'Hi',
            'Hello',
            'How are you?',
            'I am good',
            'Glad to hear',
            'How are you?'
        ])

        statement = Statement(text='Hello', conversation='training')
        first_response = self.chatbot.get_response(statement)
        second_response = self.chatbot.get_response(statement)

        self.assertEqual('How are you?', first_response.text)
        self.assertEqual('Hi', second_response.text)
