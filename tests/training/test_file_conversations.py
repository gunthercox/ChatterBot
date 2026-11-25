import csv
import json
from pathlib import Path
import tempfile
from unittest import TestCase

from chatterbot import ChatBot
from chatterbot.tagging import NoOpTagger
from chatterbot.trainers import CsvFileTrainer, JsonFileTrainer


FORMATS = [('csv', False), ('csv', True), ('tsv', False), ('tsv', True), ('json', False)]


class FileConversationTests(TestCase):
    def train(self, groups, extension, indexed=False, fields=('text', 'conversation')):
        bot = ChatBot('File conversations', database_uri=None, tagger=NoOpTagger(), logic_adapters=[])
        try:
            with tempfile.TemporaryDirectory() as directory:
                for index, rows in enumerate(groups):
                    path = Path(directory) / f'conversation-{index}.{extension}'
                    with path.open('w', encoding='utf-8', newline='') as stream:
                        if extension == 'json':
                            json.dump({'conversation': rows}, stream)
                        else:
                            writer = csv.writer(stream, delimiter='\t' if extension == 'tsv' else ',')
                            if not indexed:
                                writer.writerow(fields)
                            writer.writerows([[row[field] for field in fields] for row in rows])
                field_map = {field: index if indexed else field for index, field in enumerate(fields)}
                trainer_class = JsonFileTrainer if extension == 'json' else CsvFileTrainer
                trainer = trainer_class(bot, field_map=field_map, file_extension=extension,
                                        show_training_progress=False)
                trainer.train(directory)
                return list(bot.storage.filter(order_by=['id']))
        finally:
            bot.storage.close()

    def assert_links(self, records, expected):
        actual = {record.text: (record.in_response_to, record.search_in_response_to) for record in records}
        self.assertEqual(actual, {text: (previous, previous or '') for text, previous in expected.items()})

    def test_separate_conversations_do_not_link_to_each_other(self):
        rows = [
            {'text': 'Alpha starts', 'conversation': 'alpha'},
            {'text': 'Alpha replies', 'conversation': 'alpha'},
            {'text': 'Beta starts', 'conversation': 'beta'},
            {'text': 'Beta replies', 'conversation': 'beta'},
        ]
        for extension, indexed in FORMATS:
            with self.subTest(extension=extension, indexed=indexed):
                records = self.train([rows], extension, indexed)
                self.assert_links(records, {'Alpha starts': None, 'Alpha replies': 'Alpha starts',
                                            'Beta starts': None, 'Beta replies': 'Beta starts'})
                self.assertEqual([record.conversation for record in records], ['alpha', 'alpha', 'beta', 'beta'])

    def test_interleaved_rows_keep_each_conversations_previous_statement(self):
        rows = [
            {'text': 'Alpha starts', 'conversation': 'alpha'},
            {'text': 'Beta starts', 'conversation': 'beta'},
            {'text': 'Alpha replies', 'conversation': 'alpha'},
            {'text': 'Beta replies', 'conversation': 'beta'},
        ]
        for extension, indexed in FORMATS:
            with self.subTest(extension=extension, indexed=indexed):
                self.assert_links(self.train([rows], extension, indexed), {
                    'Alpha starts': None, 'Alpha replies': 'Alpha starts',
                    'Beta starts': None, 'Beta replies': 'Beta starts',
                })

    def test_without_a_conversation_field_rows_still_form_one_chain(self):
        rows = [{'text': 'Hello'}, {'text': 'Hi'}]
        for extension, indexed in FORMATS:
            with self.subTest(extension=extension, indexed=indexed):
                records = self.train([rows], extension, indexed, fields=('text',))
                self.assert_links(records, {'Hello': None, 'Hi': 'Hello'})
                self.assertEqual([record.conversation for record in records], ['training', 'training'])

    def test_explicit_response_fields_keep_the_supplied_links(self):
        rows = [
            {'text': 'Alpha reply', 'conversation': 'alpha', 'in_response_to': 'External prompt'},
            {'text': 'Beta reply', 'conversation': 'beta', 'in_response_to': 'Another prompt'},
        ]
        for extension, indexed in FORMATS:
            with self.subTest(extension=extension, indexed=indexed):
                records = self.train([rows], extension, indexed, fields=('text', 'conversation', 'in_response_to'))
                self.assert_links(records, {'Alpha reply': 'External prompt', 'Beta reply': 'Another prompt'})

    def test_chains_reset_for_each_input_file(self):
        groups = [[{'text': text, 'conversation': 'same'} for text in pair]
                  for pair in (('First prompt', 'First reply'), ('Second prompt', 'Second reply'))]
        for extension, indexed in FORMATS:
            with self.subTest(extension=extension, indexed=indexed):
                self.assert_links(self.train(groups, extension, indexed), {
                    'First prompt': None, 'First reply': 'First prompt',
                    'Second prompt': None, 'Second reply': 'Second prompt',
                })
