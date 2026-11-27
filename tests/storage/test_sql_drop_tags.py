from unittest import TestCase

from chatterbot.ext.sqlalchemy_app.models import Tag, tag_association_table
from chatterbot.storage.sql_storage import SQLStorageAdapter


class SQLDropTagsTests(TestCase):

    def setUp(self):
        self.adapter = SQLStorageAdapter(
            database_uri=None, raise_on_missing_search_text=False
        )
        self.addCleanup(self.adapter.close)

    def test_drop_clears_tag_associations(self):
        self.adapter.create(text='First', tags=['shared', 'first'])
        self.adapter.create(text='Second', tags=['shared'])

        self.adapter.drop()

        self.assertEqual(self.adapter.count(), 0)
        with self.adapter.Session() as session:
            self.assertEqual(session.query(Tag).count(), 0)
            self.assertEqual(
                session.execute(tag_association_table.select()).all(), []
            )

        self.adapter.drop()
        self.assertEqual(self.adapter.count(), 0)

    def test_new_statements_do_not_inherit_links_after_drop(self):
        self.adapter.create(text='Old statement', tags=['old tag'])
        self.adapter.drop()

        untagged = self.adapter.create(text='New untagged statement')
        tagged = self.adapter.create(text='New tagged statement', tags=['new tag'])

        untagged_result, = self.adapter.filter(id=untagged.id)
        tagged_result, = self.adapter.filter(id=tagged.id)
        self.assertEqual(untagged_result.get_tags(), [])
        self.assertEqual(tagged_result.get_tags(), ['new tag'])

    def test_drop_with_foreign_key_enforcement(self):
        with self.adapter.engine.connect() as connection:
            connection.exec_driver_sql('PRAGMA foreign_keys=ON')
            self.assertEqual(
                connection.exec_driver_sql('PRAGMA foreign_keys').scalar(), 1
            )

        self.adapter.create(text='Tagged statement', tags=['example'])
        self.adapter.drop()

        self.assertEqual(self.adapter.count(), 0)
        self.adapter.create(text='New statement', tags=['example'])
        self.assertEqual(self.adapter.count(), 1)
