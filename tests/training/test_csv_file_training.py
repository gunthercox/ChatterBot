import os
from tests.base_case import ChatBotTestCase
from chatterbot.trainers import CsvFileTrainer


class CsvFileTrainerTestCase(ChatBotTestCase):
    """
    Test training from CSV files.
    """

    def setUp(self):
        super().setUp()

        current_directory = os.path.dirname(os.path.abspath(__file__))

        data_file_path = os.path.join(
            current_directory,
            'test_data/csv_corpus/'
        )

        self.trainer = CsvFileTrainer(
            self.chatbot,
            data_path=data_file_path,
            show_training_progress=False,
            field_map={
                'created_at': 0,
                'persona': 1,
                'text': 2,
                'conversation': 3
            }
        )

    def test_train(self):
        """
        Test that the chat bot is trained using data from the CSV files.
        """
        self.trainer.train()

        response = self.chatbot.get_response('Is anyone there?')
        self.assertEqual(response.text, 'Yes')

    def test_train_sets_search_text(self):
        """
        Test that the chat bot is trained using data from the CSV files.
        """
        self.trainer.train()

        results = list(self.chatbot.storage.filter(text='Is anyone there?'))

        self.assertEqual(len(results), 2, msg='Results: {}'.format(results))
        self.assertEqual(results[0].search_text, 'AUX:anyone PRON:there')

    def test_train_sets_search_in_response_to(self):
        """
        Test that the chat bot is trained using data from the CSV files.
        """
        self.trainer.train()

        results = list(self.chatbot.storage.filter(in_response_to='Is anyone there?'))

        self.assertEqual(len(results), 2)
        self.assertEqual(results[0].search_in_response_to, 'AUX:anyone PRON:there')
