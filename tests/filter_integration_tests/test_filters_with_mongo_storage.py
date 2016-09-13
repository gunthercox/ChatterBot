from chatterbot.adapters.storage import MongoDatabaseAdapter
from tests.base_case import ChatBotMongoTestCase


class RepetitiveResponseFilterTestCase(ChatBotMongoTestCase):

    def test_filter_selection(self):
        from chatterbot.filters import RepetitiveResponseFilter
        from chatterbot.trainers import ListTrainer

        self.chatbot.filters = (RepetitiveResponseFilter(), )
        self.chatbot.set_trainer(ListTrainer)

        self.chatbot.train([
            'Hello',
            'Hi',
            'Hello',
            'Hi',
            'Hello',
            'Hi, how are you?',
            'I am good.'
        ])

        first_response = self.chatbot.get_response('Hello')
        second_response = self.chatbot.get_response('Hello')

        self.assertEqual(first_response.text, 'Hi')
        self.assertEqual(second_response.text, 'Hi, how are you?')

