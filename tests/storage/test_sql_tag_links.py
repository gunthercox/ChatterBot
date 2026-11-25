from unittest import TestCase

from chatterbot.conversation import Statement
from chatterbot.ext.sqlalchemy_app.models import Tag, tag_association_table
from chatterbot.storage.sql_storage import SQLStorageAdapter


class SQLTagLinksTests(TestCase):

    def setUp(self):
        self.adapter = SQLStorageAdapter(
            database_uri=None, raise_on_missing_search_text=False
        )
        self.addCleanup(self.adapter.close)

    def assert_unique_links(self, count):
        with self.adapter.engine.connect() as connection:
            links = connection.execute(tag_association_table.select()).all()
        self.assertEqual(len(links), count)
        self.assertEqual(len(set(links)), count)

    def test_repeated_updates_do_not_repeat_existing_links(self):
        statement = self.adapter.create(text='Example', tags=['original'])
        statement.add_tags('original', 'new', 'new')

        self.adapter.update(statement)
        self.adapter.update(statement)

        self.assert_unique_links(2)
        result, = self.adapter.filter(id=statement.id)
        self.assertCountEqual(result.get_tags(), ['original', 'new'])

    def test_update_new_statement_with_duplicate_tags(self):
        statement = Statement(text='New example', tags=['new', 'new'])

        self.adapter.update(statement)

        self.assert_unique_links(1)
        result, = self.adapter.filter(text=statement.text)
        self.assertEqual(result.get_tags(), ['new'])

    def test_update_retains_tags_missing_from_the_input(self):
        original = self.adapter.create(text='Example', tags=['original'])
        statement = Statement(
            id=original.id, text=original.text, tags=['new', 'new']
        )

        self.adapter.update(statement)

        self.assert_unique_links(2)
        result, = self.adapter.filter(id=original.id)
        self.assertCountEqual(result.get_tags(), ['original', 'new'])

    def test_bulk_create_deduplicates_links_and_reuses_tags(self):
        self.adapter.create(text='Existing', tags=['shared'])

        self.adapter.create_many([
            Statement(text='First', tags=['shared', 'shared', 'new', 'new']),
            Statement(text='Second', tags=['new', 'new']),
        ])

        self.assert_unique_links(4)
        with self.adapter.Session() as session:
            self.assertEqual(session.query(Tag).count(), 2)
        first, = self.adapter.filter(text='First')
        second, = self.adapter.filter(text='Second')
        self.assertCountEqual(first.get_tags(), ['shared', 'new'])
        self.assertEqual(second.get_tags(), ['new'])
