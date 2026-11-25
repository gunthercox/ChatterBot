from unittest import TestCase

from chatterbot.storage import SQLStorageAdapter


class SQLPersonaPrefixTests(TestCase):

    def setUp(self):
        self.adapter = SQLStorageAdapter(
            database_uri=None, raise_on_missing_search_text=False,
        )
        self.addCleanup(self.adapter.close)

    def test_excludes_the_requested_persona_prefix(self):
        personas = {'bot:helper', 'user:alice', 'staff:admin', ''}
        for persona in personas:
            self.adapter.create(text='Hello', persona=persona)

        for prefix in ('user:', 'staff:', 'bot:'):
            with self.subTest(prefix=prefix):
                results = self.adapter.filter(persona_not_startswith=prefix)
                self.assertEqual(
                    {statement.persona for statement in results},
                    {persona for persona in personas if not persona.startswith(prefix)},
                )

    def test_prefix_treats_sql_wildcards_as_literal_characters(self):
        personas = {'team_one', 'team%one', 'teamXone', 'bot:helper'}
        for persona in personas:
            self.adapter.create(text='Hello', persona=persona)

        for prefix in ('team_', 'team%'):
            with self.subTest(prefix=prefix):
                results = self.adapter.filter(persona_not_startswith=prefix)
                self.assertEqual(
                    {statement.persona for statement in results},
                    personas - {prefix + 'one'},
                )

    def test_prefix_combines_with_other_statement_filters(self):
        self.adapter.create(text='Keep', persona='bot:helper', conversation='current')
        self.adapter.create(text='Exclude', persona='user:alice', conversation='current')
        self.adapter.create(text='Other conversation', persona='bot:helper', conversation='other')

        results = self.adapter.filter(
            persona_not_startswith='user:', conversation='current',
        )

        self.assertEqual([statement.text for statement in results], ['Keep'])
