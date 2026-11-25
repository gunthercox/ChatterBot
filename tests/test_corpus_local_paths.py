import os
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase

from chatterbot import corpus


class LocalCorpusPathTests(TestCase):

    def setUp(self):
        temporary = TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        previous_directory = os.getcwd()
        self.addCleanup(os.chdir, previous_directory)
        os.chdir(temporary.name)

    def write_corpus(self, path):
        Path(path).write_text(
            'categories:\n- example\nconversations:\n- - Hello\n  - Hi\n',
            encoding='utf-8',
        )

    def test_load_filename_from_the_current_directory(self):
        filename = 'custom.corpus.yml'
        self.write_corpus(filename)

        files = corpus.list_corpus_files(filename)
        loaded = list(corpus.load_corpus(*files))

        self.assertEqual(files, [filename])
        self.assertEqual(loaded, [([['Hello', 'Hi']], ['example'], filename)])

    def test_load_directory_with_dots_in_its_name(self):
        directory = Path('training.data')
        (directory / 'nested').mkdir(parents=True)
        self.write_corpus(directory / 'first.yml')
        self.write_corpus(directory / 'nested' / 'second.yml')

        files = corpus.list_corpus_files(str(directory))
        loaded = list(corpus.load_corpus(*files))

        self.assertEqual(files, [
            os.path.join('training.data', 'first.yml'),
            os.path.join('training.data', 'nested', 'second.yml'),
        ])
        self.assertEqual(len(loaded), 2)
        for conversations, categories, _path in loaded:
            self.assertEqual(conversations, [['Hello', 'Hi']])
            self.assertEqual(categories, ['example'])

    def test_dotted_package_paths_still_resolve(self):
        files = corpus.list_corpus_files('chatterbot.corpus.english.greetings')
        loaded = list(corpus.load_corpus(*files))

        self.assertEqual(len(loaded), 1)
        conversations, categories, _path = loaded[0]
        self.assertIn(['Hi', 'Hello'], conversations)
        self.assertEqual(categories, ['greetings'])
