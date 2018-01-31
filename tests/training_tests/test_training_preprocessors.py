from tests.base_case import ChatBotTestCase
from chatterbot import trainers
from chatterbot import preprocessors


class PreprocessorTrainingTests(ChatBotTestCase):
    """
    These tests are designed to ensure that preprocessors
    will be used to process the input the chat bot is given
    during the training process.
    """

    def test_training_cleans_whitespace(self):
        """
        Test that the ``clean_whitespace`` preprocessor is used during
        the training process.
        """
        self.chatbot.preprocessors = [preprocessors.clean_whitespace]
        self.chatbot.set_trainer(
            trainers.ListTrainer,
            show_training_progress=False
        )

        self.chatbot.train([
            'Can I help you with anything?',
            'No, I     think I am all set.',
            'Okay, have a nice day.',
            'Thank you, you too.'
        ])

        response = self.chatbot.get_response('Can I help you with anything?')

        self.assertEqual(response.text, 'No, I think I am all set.')
