from pathlib import Path
import sqlite3
from tempfile import TemporaryDirectory
from unittest import TestCase

from sqlalchemy import create_engine

from chatterbot.storage import SQLStorageAdapter


class SQLConnectionEventTests(TestCase):

    def test_unrelated_engine_keeps_sqlite_defaults(self):
        reference = sqlite3.connect(':memory:')
        self.addCleanup(reference.close)
        default_synchronous = reference.execute('PRAGMA synchronous').fetchone()[0]

        unrelated_engine = create_engine('sqlite://')
        self.addCleanup(unrelated_engine.dispose)
        adapter = SQLStorageAdapter(database_uri=None)
        self.addCleanup(adapter.close)

        with unrelated_engine.connect() as connection:
            self.assertEqual(
                connection.exec_driver_sql('PRAGMA synchronous').scalar(),
                default_synchronous,
            )

    def test_adapter_still_configures_its_own_connections(self):
        with TemporaryDirectory() as directory:
            database = Path(directory) / 'statements.sqlite3'
            adapter = SQLStorageAdapter(database_uri='sqlite:///' + str(database))
            try:
                # Reconnect to also exercise the listener after pool disposal.
                adapter.engine.dispose()
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
