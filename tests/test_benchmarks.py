"""
These tests are designed to test execution time for
various chat bot configurations to help prevent
performance based regressions when changes are made.
"""

from .base_case import ChatBotSQLTestCase, ChatBotMongoTestCase
from chatterbot import ChatBot
from chatterbot import utils
import sys
import logging


logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO
)

STATEMENT_LIST = utils.generate_strings(10)


class BenchmarkingMixin(object):

    def setUp(self):
        super(BenchmarkingMixin, self).setUp()

        self.logger = logging.getLogger(__name__)

    def get_kwargs(self):
        kwargs = super(BenchmarkingMixin, self).get_kwargs()
        kwargs['trainer'] = 'chatterbot.trainers.ListTrainer'
        kwargs['show_training_progress'] = False
        return kwargs

    def assert_response_duration(self, maximum_duration, test_kwargs):
        """
        Assert that the response time did not exceed the maximum allowed amount.
        """

        chatbot = ChatBot('Benchmark', **test_kwargs)
        chatbot.train(STATEMENT_LIST)

        duration = utils.get_response_time(chatbot)

        self.logger.info('Duration was %f seconds' % duration)

        if duration > maximum_duration:
            raise AssertionError(
                '{duration} was greater than the maximum allowed '
                'response time of {maximum_duration}'.format(
                    duration=duration,
                    maximum_duration=maximum_duration
                )
            )


class SqlBenchmarkingTests(BenchmarkingMixin, ChatBotSQLTestCase):
    """
    Benchmarking tests for SQL storage.
    """

    def get_kwargs(self):
        kwargs = super(SqlBenchmarkingTests, self).get_kwargs()
        kwargs['storage_adapter'] = 'chatterbot.storage.SQLStorageAdapter'
        return kwargs

    def test_levenshtein_distance_comparisons(self):
        """
        Test the levenshtein distance comparison algorithm.
        """
        kwargs = self.get_kwargs()
        kwargs.update({
            'logic_adapters': [
                {
                    'import_path': 'chatterbot.logic.BestMatch',
                    'statement_comparison_function': 'chatterbot.comparisons.levenshtein_distance',
                    'response_selection_method': 'chatterbot.response_selection.get_first_response'
                }
            ]
        })

        self.assert_response_duration(1, kwargs)

    def test_synset_distance_comparisons(self):
        """
        Test the synset distance comparison algorithm.
        """
        kwargs = self.get_kwargs()
        kwargs.update({
            'logic_adapters': [
                {
                    'import_path': 'chatterbot.logic.BestMatch',
                    'statement_comparison_function': 'chatterbot.comparisons.synset_distance',
                    'response_selection_method': 'chatterbot.response_selection.get_first_response'
                }
            ]
        })

        self.assert_response_duration(1.9, kwargs)

    def test_english_corpus_training(self):
        """
        Test the amount of time it takes to train with the English corpus.
        """
        import unittest
        raise unittest.SkipTest('TODO: This test needs to be written.')


class MongoBenchmarkingTests(BenchmarkingMixin, ChatBotMongoTestCase):
    """
    Benchmarking tests for Mongo DB storage.
    """

    def get_kwargs(self):
        kwargs = super(MongoBenchmarkingTests, self).get_kwargs()
        kwargs['storage_adapter'] = 'chatterbot.storage.MongoDatabaseAdapter'
        return kwargs

    def test_levenshtein_distance_comparisons(self):
        """
        Test the levenshtein distance comparison algorithm.
        """
        kwargs = self.get_kwargs()
        kwargs.update({
            'logic_adapters': [
                {
                    'import_path': 'chatterbot.logic.BestMatch',
                    'statement_comparison_function': 'chatterbot.comparisons.levenshtein_distance',
                    'response_selection_method': 'chatterbot.response_selection.get_first_response'
                }
            ]
        })

        self.assert_response_duration(1, kwargs)

    def test_synset_distance_comparisons(self):
        """
        Test the synset distance comparison algorithm.
        """
        kwargs = self.get_kwargs()
        kwargs.update({
            'logic_adapters': [
                {
                    'import_path': 'chatterbot.logic.BestMatch',
                    'statement_comparison_function': 'chatterbot.comparisons.synset_distance',
                    'response_selection_method': 'chatterbot.response_selection.get_first_response'
                }
            ]
        })

        self.assert_response_duration(1.9, kwargs)

    def test_english_corpus_training(self):
        """
        Test the amount of time it takes to train with the English corpus.
        """
        import unittest
        raise unittest.SkipTest('TODO: This test needs to be written.')
