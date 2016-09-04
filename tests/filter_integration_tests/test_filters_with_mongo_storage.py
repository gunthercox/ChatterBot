from chatterbot.adapters.storage import MongoDatabaseAdapter
from tests.base_case import ChatBotMongoTestCase


class RepetitiveResponseFilterTestCase(ChatBotMongoTestCase):

    def test_filter_selection(self):
        from chatterbot.filters import RepetitiveResponseFilter
        from chatterbot.trainers import ListTrainer

        self.chatbot.filters.append(RepetitiveResponseFilter)
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


class LanguageFilterTestCase(ChatBotMongoTestCase):

    def test_filter_selection(self):
        from chatterbot.filters import LanguageFilter
        from chatterbot.trainers import ListTrainer

        self.chatbot.filters.append(LanguageFilter)
        self.chatbot.set_trainer(ListTrainer)

        self.chatbot.train([
            'Look over there at that pile of crap!',
            'Wow, that is a lot shit.',
            'Dammit! Who is going to clean that up?'
        ])

        self.chatbot.train([
            'Look at that pile of crap!',
            'Wow, that is a lot poop.',
            'Who is going to clean that up?'
        ])

        # Check that the bot avoids responses with swears
        response = self.chatbot.get_response(
            'Look over there at that pile of crap!'
        )

        self.assertEqual(response.text, 'Wow, that is a lot poop.')

