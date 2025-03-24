import os
from tests.base_case import ChatBotTestCase
from chatterbot.trainers import JsonFileTrainer


class JsonFileTrainerTestCase(ChatBotTestCase):
    """
    Test training from JSON files.
    """

    def setUp(self):
        super().setUp()

        current_directory = os.path.dirname(os.path.abspath(__file__))

        self.data_file_path = os.path.join(
            current_directory,
            'test_data/json_corpus/'
        )

        self.trainer = JsonFileTrainer(
            self.chatbot,
            show_training_progress=False,
            field_map={
                'persona': 'persona',
                'text': 'text',
                'conversation': 'conversation',
                'in_response_to': 'in_response_to',
            }
        )

    def test_train(self):
        """
        Test that the chat bot is trained using data from the JSON files.
        """
        self.trainer.train(self.data_file_path)

        response = self.chatbot.get_response('Is anyone there?')
        self.assertEqual(response.text, 'Yes')

    def test_train_sets_search_text(self):
        """
        Test that the chat bot is trained using data from the JSON files.
        """
        self.trainer.train(self.data_file_path)

        results = list(self.chatbot.storage.filter(text='Is anyone there?'))

        self.assertEqual(len(results), 2, msg='Results: {}'.format(results))
        self.assertEqual(results[0].search_text, 'AUX:anyone PRON:there')

    def test_train_sets_search_in_response_to(self):
        """
        Test that the chat bot is trained using data from the JSON files.
        """
        self.trainer.train(self.data_file_path)

        results = list(self.chatbot.storage.filter(in_response_to='Is anyone there?'))

        self.assertEqual(len(results), 2)
        self.assertEqual(results[0].search_in_response_to, 'AUX:anyone PRON:there')
