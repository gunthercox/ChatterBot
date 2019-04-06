"""
These tests are designed to test execution time for
various chat bot configurations to help prevent
performance based regressions when changes are made.
"""

from unittest import skip
from warnings import warn
from random import choice
from tests.base_case import ChatBotSQLTestCase, ChatBotMongoTestCase
from chatterbot.trainers import ListTrainer, ChatterBotCorpusTrainer, UbuntuCorpusTrainer
from chatterbot.logic import BestMatch
from chatterbot import comparisons, response_selection, utils


WORDBANK = (
    'the', 'mellifluous', 'sound', 'of', 'a', 'spring', 'evening',
    'breaks', 'the', 'heart', 'string', 'by', 'calling', 'out', 'to',
    'David', 'who', 'looks', 'on', 'at', 'the', 'world', 'blankly',
    'who', 'could', 'tell', 'that', 'there', 'is', 'no', 'instrament',
    'softly', 'strumming', 'toward', 'the', 'melody', 'called', 'silence',
)


# Generate a list of random sentences
STATEMENT_LIST = [
    '{:s} {:s} {:s} {:s} {:s} {:s} {:s} {:s} {:s} {:s}'.format(
        *[choice(WORDBANK) for __ in range(0, 10)]
    ) for _ in range(0, 10)
]


def get_list_trainer(chatbot):
    return ListTrainer(
        chatbot,
        show_training_progress=False
    )


def get_chatterbot_corpus_trainer(chatbot):
    return ChatterBotCorpusTrainer(
        chatbot,
        show_training_progress=False
    )


def get_ubuntu_corpus_trainer(chatbot):
    return UbuntuCorpusTrainer(
        chatbot,
        show_training_progress=False
    )


class BenchmarkingMixin(object):

    def assert_response_duration_is_less_than(self, maximum_duration, strict=False):
        """
        Assert that the response time did not exceed the maximum allowed amount.

        :param strict: If set to true, test will fail if the maximum duration is exceeded.
        """
        from sys import stdout

        duration = utils.get_response_time(self.chatbot)

        stdout.write('\nBENCHMARK: Duration was %f seconds\n' % duration)

        failure_message = (
            '{duration} was greater than the maximum allowed '
            'response time of {maximum_duration}'.format(
                duration=duration,
                maximum_duration=maximum_duration
            )
        )

        if strict and duration > maximum_duration:
            raise AssertionError(failure_message)
        elif duration > maximum_duration:
            warn(failure_message)


class SqlBenchmarkingTests(BenchmarkingMixin, ChatBotSQLTestCase):
    """
    Benchmarking tests for SQL storage.
    """

    def get_kwargs(self):
        kwargs = super().get_kwargs()
        kwargs['storage_adapter'] = 'chatterbot.storage.SQLStorageAdapter'
        return kwargs

    def test_levenshtein_distance_comparisons(self):
        """
        Test the levenshtein distance comparison algorithm.
        """
        self.chatbot.logic_adapters[0] = BestMatch(
            self.chatbot,
            statement_comparison_function=comparisons.LevenshteinDistance,
            response_selection_method=response_selection.get_first_response
        )

        trainer = get_list_trainer(self.chatbot)
        trainer.train(STATEMENT_LIST)

        self.assert_response_duration_is_less_than(1)

    def test_spacy_similarity_comparisons(self):
        """
        Test the spacy similarity comparison algorithm.
        """
        self.chatbot.logic_adapters[0] = BestMatch(
            self.chatbot,
            statement_comparison_function=comparisons.SpacySimilarity,
            response_selection_method=response_selection.get_first_response
        )

        trainer = get_list_trainer(self.chatbot)
        trainer.train(STATEMENT_LIST)

        self.assert_response_duration_is_less_than(3)

    def test_get_response_after_chatterbot_corpus_training(self):
        """
        Test response time after training with the ChatterBot corpus.
        """
        trainer = get_chatterbot_corpus_trainer(self.chatbot)
        trainer.train('chatterbot.corpus')

        self.assert_response_duration_is_less_than(3)

    @skip('Test marked as skipped due to execution time.')
    def test_get_response_after_ubuntu_corpus_training(self):
        """
        Test response time after training with the Ubuntu corpus.
        """
        trainer = get_ubuntu_corpus_trainer(self.chatbot)
        trainer.train()

        self.assert_response_duration_is_less_than(6)


class MongoBenchmarkingTests(BenchmarkingMixin, ChatBotMongoTestCase):
    """
    Benchmarking tests for Mongo DB storage.
    """

    def get_kwargs(self):
        kwargs = super().get_kwargs()
        kwargs['storage_adapter'] = 'chatterbot.storage.MongoDatabaseAdapter'
        return kwargs

    def test_levenshtein_distance_comparisons(self):
        """
        Test the levenshtein distance comparison algorithm.
        """
        self.chatbot.logic_adapters[0] = BestMatch(
            self.chatbot,
            statement_comparison_function=comparisons.LevenshteinDistance,
            response_selection_method=response_selection.get_first_response
        )

        trainer = get_list_trainer(self.chatbot)
        trainer.train(STATEMENT_LIST)

        self.assert_response_duration_is_less_than(1)

    def test_spacy_similarity_comparisons(self):
        """
        Test the spacy similarity comparison algorithm.
        """
        self.chatbot.logic_adapters[0] = BestMatch(
            self.chatbot,
            statement_comparison_function=comparisons.SpacySimilarity,
            response_selection_method=response_selection.get_first_response
        )

        trainer = get_list_trainer(self.chatbot)
        trainer.train(STATEMENT_LIST)

        self.assert_response_duration_is_less_than(3)

    def test_get_response_after_chatterbot_corpus_training(self):
        """
        Test response time after training with the ChatterBot corpus.
        """
        trainer = get_chatterbot_corpus_trainer(self.chatbot)
        trainer.train('chatterbot.corpus')

        self.assert_response_duration_is_less_than(3)

    @skip('Test marked as skipped due to execution time.')
    def test_get_response_after_ubuntu_corpus_training(self):
        """
        Test response time after training with the Ubuntu corpus.
        """
        trainer = get_ubuntu_corpus_trainer(self.chatbot)
        trainer.train()

        self.assert_response_duration_is_less_than(6)
