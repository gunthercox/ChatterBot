import os
import io
from unittest import TestCase
from chatterbot import corpus


class CorpusLoadingTestCase(TestCase):

    def test_load_corpus_chinese(self):
        corpus_data = corpus.load_corpus('chatterbot.corpus.chinese')

        self.assertTrue(len(list(corpus_data)))

    def test_load_corpus_english(self):
        corpus_data = corpus.load_corpus('chatterbot.corpus.english')

        self.assertTrue(len(list(corpus_data)))

    def test_load_corpus_english_greetings(self):
        corpus_data = list(
            corpus.load_corpus('chatterbot.corpus.english.greetings')
        )

        self.assertEqual(len(corpus_data), 1)

        conversations, categories, file_path = corpus_data[0]

        self.assertIn(['Hi', 'Hello'], conversations)
        self.assertEqual(['greetings'], categories)
        self.assertIn('chatterbot_corpus/data/english/greetings.yml', file_path)

    def test_load_corpus_english_categories(self):
        corpus_data = list(
            corpus.load_corpus('chatterbot.corpus.english.greetings')
        )

        self.assertEqual(len(corpus_data), 1)

        # Test that each conversation gets labeled with the correct category
        for _conversation, categories, _file_path in corpus_data:
            self.assertIn('greetings', categories)

    def test_load_corpus_french(self):
        corpus_data = corpus.load_corpus('chatterbot.corpus.french')

        self.assertTrue(len(list(corpus_data)))

    def test_load_corpus_german(self):
        corpus_data = corpus.load_corpus('chatterbot.corpus.german')

        self.assertTrue(len(list(corpus_data)))

    def test_load_corpus_hindi(self):
        corpus_data = corpus.load_corpus('chatterbot.corpus.hindi')

        self.assertTrue(len(list(corpus_data)))

    def test_load_corpus_indonesia(self):
        corpus_data = corpus.load_corpus('chatterbot.corpus.indonesia')

        self.assertTrue(len(list(corpus_data)))

    def test_load_corpus_italian(self):
        corpus_data = corpus.load_corpus('chatterbot.corpus.italian')

        self.assertTrue(len(list(corpus_data)))

    def test_load_corpus_marathi(self):
        corpus_data = corpus.load_corpus('chatterbot.corpus.marathi')

        self.assertTrue(len(list(corpus_data)))

    def test_load_corpus_portuguese(self):
        corpus_data = corpus.load_corpus('chatterbot.corpus.portuguese')

        self.assertTrue(len(list(corpus_data)))

    def test_load_corpus_russian(self):
        corpus_data = corpus.load_corpus('chatterbot.corpus.russian')

        self.assertTrue(len(list(corpus_data)))

    def test_load_corpus_spanish(self):
        corpus_data = corpus.load_corpus('chatterbot.corpus.spanish')

        self.assertTrue(len(list(corpus_data)))

    def test_load_corpus_telugu(self):
        corpus_data = corpus.load_corpus('chatterbot.corpus.telugu')

        self.assertTrue(len(list(corpus_data)))


class CorpusUtilsTestCase(TestCase):

    def test_get_file_path(self):
        """
        Test that a dotted path is properly converted to a file address.
        """
        path = corpus.get_file_path('chatterbot.corpus.english')
        self.assertIn(
            os.path.join('chatterbot_corpus', 'data', 'english'),
            path
        )

    def test_read_english_corpus(self):
        corpus_path = os.path.join(
            corpus.DATA_DIRECTORY,
            'english', 'conversations.yml'
        )
        data = corpus.read_corpus(corpus_path)
        self.assertIn('conversations', data)

    def test_list_english_corpus_files(self):
        data_files = corpus.list_corpus_files('chatterbot.corpus.english')

        self.assertIn('.yml', data_files[0])

    def test_load_corpus(self):
        """
        Test loading the entire corpus of languages.
        """
        corpus_data = corpus.load_corpus('chatterbot.corpus')

        self.assertTrue(len(list(corpus_data)))


class CorpusFilePathTestCase(TestCase):

    def test_load_corpus_file(self):
        """
        Test that a file path can be specified for a corpus.
        """

        # Create a file for testing
        file_path = './test_corpus.yml'
        with io.open(file_path, 'w') as test_corpus:
            yml_data = u'\n'.join(
                ['conversations:', '- - Hello', '  - Hi', '- - Hi', '  - Hello']
            )
            test_corpus.write(yml_data)

        corpus_data = list(corpus.load_corpus(file_path))

        # Remove the test file
        if os.path.exists(file_path):
            os.remove(file_path)

        self.assertEqual(len(corpus_data), 1)

        # Load the content from the corpus
        conversations, _categories, _file_path = corpus_data[0]

        self.assertEqual(len(conversations[0]), 2)

    def test_load_corpus_file_non_existent(self):
        """
        Test that a file path can be specified for a corpus.
        """
        file_path = './test_corpus.yml'

        self.assertFalse(os.path.exists(file_path))
        with self.assertRaises(IOError):
            list(corpus.load_corpus(file_path))

    def test_load_corpus_english_greetings(self):
        file_path = os.path.join(corpus.DATA_DIRECTORY, 'english', 'greetings.yml')

        corpus_data = corpus.load_corpus(file_path)

        self.assertEqual(len(list(corpus_data)), 1)

    def test_load_corpus_english(self):
        file_path = os.path.join(corpus.DATA_DIRECTORY, 'english')

        corpus_data = corpus.load_corpus(file_path)

        self.assertGreater(len(list(corpus_data)), 1)

    def test_load_corpus_english_trailing_slash(self):
        file_path = os.path.join(corpus.DATA_DIRECTORY, 'english') + '/'

        corpus_data = list(corpus.load_corpus(file_path))

        self.assertGreater(len(list(corpus_data)), 1)
