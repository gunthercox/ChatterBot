from unittest import TestCase

from chatterbot.storage.sql_storage import SQLStorageAdapter


class SQLLiteralSubstringTests(TestCase):

    def setUp(self):
        self.adapter = SQLStorageAdapter(
            database_uri=None, raise_on_missing_search_text=False
        )
        self.addCleanup(self.adapter.close)

    def test_search_filters_match_literal_wildcard_characters(self):
        for field in ('search_text', 'search_in_response_to'):
            for literal, other in (
                ('20%', '200'),
                ('field_name', 'fieldXname'),
                ('path/_part', 'path/xpart'),
            ):
                with self.subTest(field=field, literal=literal):
                    self.adapter.drop()
                    self.adapter.create(text='Literal', **{field: literal})
                    self.adapter.create(text='Other', **{field: other})

                    results = list(self.adapter.filter(**{
                        field + '_contains': literal
                    }))

                    self.assertEqual([item.text for item in results], ['Literal'])

    def test_exclusions_match_literal_wildcard_characters(self):
        for literal, other in (
            ('20%', '200'),
            ('field_name', 'fieldXname'),
            ('path/_part', 'path/xpart'),
        ):
            with self.subTest(literal=literal):
                self.adapter.drop()
                self.adapter.create(text='Contains ' + literal)
                self.adapter.create(text='Contains ' + other)

                results = list(self.adapter.filter(exclude_text_words=[literal]))

                self.assertEqual([item.text for item in results], ['Contains ' + other])

    def test_exclusions_remain_case_insensitive_and_match_any_word(self):
        self.adapter.create(text='MODEL_A is unavailable')
        self.adapter.create(text='An ALTERNATIVE is unavailable')
        self.adapter.create(text='modelXa is available')

        results = list(self.adapter.filter(
            exclude_text_words=['model_a', 'alternative']
        ))

        self.assertEqual([item.text for item in results], ['modelXa is available'])

    def test_search_filters_still_match_any_term(self):
        for field in ('search_text', 'search_in_response_to'):
            with self.subTest(field=field):
                self.adapter.drop()
                self.adapter.create(text='First', **{field: 'known_value'})
                self.adapter.create(text='Second', **{field: 'alternate'})
                self.adapter.create(text='Other', **{field: 'knownXvalue'})

                results = list(self.adapter.filter(**{
                    field + '_contains': 'known_value alternate'
                }))

                self.assertCountEqual([item.text for item in results], ['First', 'Second'])
