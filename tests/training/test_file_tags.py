import csv
import json
from pathlib import Path
import tempfile
from unittest import TestCase

from chatterbot import ChatBot
from chatterbot.tagging import NoOpTagger
from chatterbot.trainers import CsvFileTrainer, JsonFileTrainer


FORMATS = [('csv', False), ('csv', True), ('tsv', False), ('tsv', True), ('json', False)]


class FileTagTests(TestCase):
    def train(self, tags, extension, indexed=False, map_tags=True):
        bot = ChatBot('File tags', database_uri=None, tagger=NoOpTagger(), logic_adapters=[])
        try:
            with tempfile.TemporaryDirectory() as directory:
                path = Path(directory) / f'conversation.{extension}'
                rows = [{'utterance': f'Row {index}', 'labels': value} for index, value in enumerate(tags)]
                with path.open('w', encoding='utf-8', newline='') as stream:
                    if extension == 'json':
                        json.dump({'conversation': rows}, stream)
                    else:
                        writer = csv.writer(stream, delimiter='\t' if extension == 'tsv' else ',')
                        if not indexed:
                            writer.writerow(['utterance', 'labels'])
                        writer.writerows([[row['utterance'], row['labels']] for row in rows])
                field_map = {'text': 0 if indexed else 'utterance'}
                if map_tags:
                    field_map['tags'] = 1 if indexed else 'labels'
                trainer_class = JsonFileTrainer if extension == 'json' else CsvFileTrainer
                trainer = trainer_class(bot, field_map=field_map, file_extension=extension,
                                        show_training_progress=False)
                trainer.train(str(path))
                records = list(bot.storage.filter(order_by=['id']))
                matching = [record.text for record in bot.storage.filter(tags=['support'])]
                return records, matching
        finally:
            bot.storage.close()

    def test_string_labels_are_saved_as_whole_tags(self):
        labels = ['support', '售后支持', 'billing, refunds', ' padded tag ']
        for extension, indexed in FORMATS:
            with self.subTest(extension=extension, indexed=indexed):
                records, matching = self.train(labels, extension, indexed)
                self.assertEqual({record.text: record.get_tags() for record in records},
                                 {f'Row {index}': [label] for index, label in enumerate(labels)})
                self.assertEqual(matching, ['Row 0'])

    def test_an_empty_cell_means_no_tags(self):
        for extension, indexed in FORMATS:
            with self.subTest(extension=extension, indexed=indexed):
                records, matching = self.train([''], extension, indexed)
                self.assertEqual(records[0].get_tags(), [])
                self.assertEqual(matching, [])

    def test_json_arrays_still_hold_multiple_tags(self):
        records, matching = self.train([['support', 'billing'], []], 'json')
        by_text = {record.text: record.get_tags() for record in records}
        self.assertEqual(set(by_text['Row 0']), {'support', 'billing'})
        self.assertEqual(by_text['Row 1'], [])
        self.assertEqual(matching, ['Row 0'])

    def test_unmapped_tag_columns_are_not_added(self):
        for extension, indexed in FORMATS:
            with self.subTest(extension=extension, indexed=indexed):
                records, matching = self.train(['support'], extension, indexed, map_tags=False)
                self.assertEqual(records[0].get_tags(), [])
                self.assertEqual(matching, [])
