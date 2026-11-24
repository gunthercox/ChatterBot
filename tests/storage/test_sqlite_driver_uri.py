from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase

from chatterbot.storage import SQLStorageAdapter


class SQLiteDriverURITests(TestCase):

    def test_file_database_uses_sqlite_pragmas(self):
        with TemporaryDirectory() as directory:
            database = Path(directory) / 'statements.sqlite3'
            adapter = SQLStorageAdapter(database_uri='sqlite+pysqlite:///' + str(database))
            try:
                with adapter.engine.connect() as connection:
                    self.assertEqual(
                        connection.exec_driver_sql('PRAGMA journal_mode').scalar(),
                        'wal',
                    )
                    self.assertEqual(
                        connection.exec_driver_sql('PRAGMA synchronous').scalar(),
                        1,
                    )
            finally:
                adapter.close()

    def test_memory_database_accepts_default_and_explicit_drivers(self):
        for uri in ('sqlite+pysqlite://', 'sqlite+pysqlite:///:memory:', 'sqlite://'):
            with self.subTest(database_uri=uri):
                adapter = SQLStorageAdapter(database_uri=uri)
                try:
                    adapter.create(text='SQLite statement', search_text='sqlite statement')

                    self.assertEqual(adapter.count(), 1)
                    self.assertEqual(adapter.get_random().text, 'SQLite statement')
                finally:
                    adapter.close()
