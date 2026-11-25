from unittest import TestCase

from sqlalchemy.exc import IntegrityError

from chatterbot.ext.sqlalchemy_app.models import Tag
from chatterbot.storage.sql_storage import SQLStorageAdapter


class SQLCreateErrorsTests(TestCase):

    def test_failed_insert_does_not_poison_the_scoped_session(self):
        adapter = SQLStorageAdapter(
            database_uri=None, raise_on_missing_search_text=False
        )
        self.addCleanup(adapter.close)
        original = adapter.create(id=1, text='Original', tags=['keep'])

        with self.assertRaises(IntegrityError):
            adapter.create(id=1, text='Duplicate ID', tags=['rolled back'])

        created = adapter.create(id=2, text='Next valid insert', tags=['new'])

        self.assertEqual(adapter.count(), 2)
        stored_original, = adapter.filter(id=original.id)
        stored_created, = adapter.filter(id=created.id)
        self.assertEqual(stored_original.text, 'Original')
        self.assertEqual(stored_original.get_tags(), ['keep'])
        self.assertEqual(stored_created.text, 'Next valid insert')
        self.assertEqual(stored_created.get_tags(), ['new'])
        with adapter.Session() as session:
            self.assertEqual(
                session.query(Tag).filter_by(name='rolled back').count(), 0
            )
