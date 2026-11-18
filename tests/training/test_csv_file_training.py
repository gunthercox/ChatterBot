import csv
import os
import tempfile
from tests.base_case import ChatBotTestCase
from chatterbot.trainers import CsvFileTrainer


class CsvFileTrainerTestCase(ChatBotTestCase):
    """
    Test training from CSV files.
    """

    def setUp(self):
        super().setUp()

        current_directory = os.path.dirname(os.path.abspath(__file__))

        self.data_file_path = os.path.join(
            current_directory,
            'test_data/csv_corpus/'
        )

        self.trainer = CsvFileTrainer(
            self.chatbot,
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
        self.trainer.train(self.data_file_path)

        response = self.chatbot.get_response('Is anyone there?')
        self.assertEqual(response.text, 'Yes')

    def test_train_sets_search_text(self):
        """
        Test that the chat bot is trained using data from the CSV files.
        """
        self.trainer.train(self.data_file_path)

        results = list(self.chatbot.storage.filter(text='Is anyone there?'))

        self.assertEqual(len(results), 2, msg='Results: {}'.format(results))
        self.assertEqual(results[0].search_text, 'AUX:anyone PRON:there')

    def test_train_sets_search_in_response_to(self):
        """
        Test that the chat bot is trained using data from the CSV files.
        """
        self.trainer.train(self.data_file_path)

        results = list(self.chatbot.storage.filter(in_response_to='Is anyone there?'))

        self.assertEqual(len(results), 2)
        self.assertEqual(results[0].search_in_response_to, 'AUX:anyone PRON:there')

    def test_train_with_explicit_responses(self):
        for extension, delimiter in [('csv', ','), ('tsv', '\t')]:
            for use_header in [True, False]:
                with self.subTest(extension=extension, use_header=use_header):
                    reply = f'Reply from {extension}, header={use_header}'
                    prompt = 'Is anyone there?'
                    field_map = {
                        'text': 'reply' if use_header else 1,
                        'in_response_to': 'prompt' if use_header else 0,
                    }
                    trainer = CsvFileTrainer(
                        self.chatbot,
                        show_training_progress=False,
                        file_extension=extension,
                        field_map=field_map,
                    )

                    with tempfile.TemporaryDirectory() as directory:
                        filename = os.path.join(directory, f'conversation.{extension}')
                        with open(filename, 'w', encoding='utf-8', newline='') as file:
                            writer = csv.writer(file, delimiter=delimiter)
                            if use_header:
                                writer.writerow(['prompt', 'reply'])
                            writer.writerow([prompt, reply])
                        trainer.train(filename)

                    results = list(self.chatbot.storage.filter(text=reply))
                    self.assertEqual(len(results), 1)
                    self.assertEqual(results[0].in_response_to, prompt)
                    self.assertEqual(results[0].search_in_response_to, 'AUX:anyone PRON:there')
