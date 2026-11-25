from unittest import TestCase

from chatterbot.conversation import Statement
from chatterbot.storage import SQLStorageAdapter


class SQLUpdateSearchTests(TestCase):

    def setUp(self):
        self.adapter = SQLStorageAdapter(database_uri=None)
        self.addCleanup(self.adapter.close)

    def assert_search_fields_saved(self, statement):
        stored, = self.adapter.filter(text=statement.text)
        self.assertEqual(stored.search_text, statement.search_text)
        self.assertEqual(stored.search_in_response_to, statement.search_in_response_to)
        self.assertEqual(
            [result.id for result in self.adapter.filter(search_text_contains=statement.search_text)],
            [stored.id],
        )
        self.assertEqual(
            [result.id for result in self.adapter.filter(
                search_in_response_to_contains=statement.search_in_response_to,
            )],
            [stored.id],
        )

    def test_update_creates_searchable_statement(self):
        statement = Statement(
            'Answer', search_text='answer-index',
            in_response_to='Question', search_in_response_to='question-index',
        )

        self.adapter.update(statement)

        self.assert_search_fields_saved(statement)

    def test_update_replaces_indexes_for_an_existing_statement_id(self):
        statement = self.adapter.create(
            text='Answer', search_text='old-answer',
            in_response_to='Old question', search_in_response_to='old-question',
        )
        statement.search_text = 'new-answer'
        statement.in_response_to = 'New question'
        statement.search_in_response_to = 'new-question'

        self.adapter.update(statement)

        self.assert_search_fields_saved(statement)
        self.assertEqual(list(self.adapter.filter(search_text_contains='old-answer')), [])
        self.assertEqual(list(self.adapter.filter(search_in_response_to_contains='old-question')), [])

    def test_update_replaces_indexes_when_matching_text_and_conversation(self):
        self.adapter.create(text='Answer', search_text='old-answer', conversation='training')
        statement = Statement(
            'Answer', search_text='new-answer', conversation='training',
            in_response_to='Question', search_in_response_to='question-index',
        )

        self.adapter.update(statement)

        self.assertEqual(self.adapter.count(), 1)
        self.assert_search_fields_saved(statement)

    def test_optional_missing_indexes_are_saved_as_empty_strings(self):
        self.adapter.raise_on_missing_search_text = False
        statement = self.adapter.create(
            text='Answer', search_text='old-answer', search_in_response_to='old-question',
        )
        statement.search_text = None
        statement.search_in_response_to = None

        self.adapter.update(statement)

        stored, = self.adapter.filter(id=statement.id)
        self.assertEqual(stored.search_text, '')
        self.assertEqual(stored.search_in_response_to, '')
