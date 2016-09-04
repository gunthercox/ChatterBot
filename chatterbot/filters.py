# Filters set the base query that gets passed to the storage adapter
import abc
import six


@six.add_metaclass(abc.ABCMeta)
class Filter(object):
    """
    A base filter object from which all other
    filters should be subclassed.
    """

    @abc.abstractmethod
    def filter_selection(self, chatterbot):
        return chatterbot.storage.base_query


class RepetitiveResponseFilter(Filter):
    """
    A filter that eliminates possibly repetitive
    responses to prevent a chat bot from repeating
    statements that it has recently said.
    """

    def filter_selection(self, chatterbot):

        if chatterbot.recent_statements.empty():
            return chatterbot.storage.base_query

        text_of_recent_responses = []

        for statement, response in chatterbot.recent_statements:
            text_of_recent_responses.append(response.text)

        query = chatterbot.storage.base_query.statement_text_not_in(
            text_of_recent_responses
        )

        return query


class LanguageFilter(Filter):
    """
    A filter that excludes swear words and explicit
    language from the selection of possible responses
    that a chat bot can respond with.
    """

    def __init__(self):
        import os
        import io

        current_directory = os.path.dirname(__file__)
        swear_words = os.path.join(
            current_directory, 'corpus', 'data', 'english', 'swear_words.csv'
        )

        with io.open(swear_words, encoding='utf-8') as data_file:
            self.words = data_file.read().split(',')

    def filter_selection(self, chatterbot):
        return chatterbot.storage.base_query.statement_text_not_in(
            self.words
        )
