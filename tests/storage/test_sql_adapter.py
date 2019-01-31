from unittest import TestCase
from chatterbot.conversation import Statement
from chatterbot.storage.sql_storage import SQLStorageAdapter


class SQLStorageAdapterTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        """
        Instantiate the adapter before any tests in the test case run.
        """
        cls.adapter = SQLStorageAdapter(database_uri=None)

    def tearDown(self):
        """
        Drop the tables in the database after each test is run.
        """
        self.adapter.drop()


class SQLStorageAdapterTests(SQLStorageAdapterTestCase):

    def test_set_database_uri_none(self):
        adapter = SQLStorageAdapter(database_uri=None)
        self.assertEqual(adapter.database_uri, 'sqlite://')

    def test_set_database_uri(self):
        adapter = SQLStorageAdapter(database_uri='sqlite:///db.sqlite3')
        self.assertEqual(adapter.database_uri, 'sqlite:///db.sqlite3')

    def test_count_returns_zero(self):
        """
        The count method should return a value of 0
        when nothing has been saved to the database.
        """
        self.assertEqual(self.adapter.count(), 0)

    def test_count_returns_value(self):
        """
        The count method should return a value of 1
        when one item has been saved to the database.
        """
        self.adapter.create(text="Test statement")
        self.assertEqual(self.adapter.count(), 1)

    def test_filter_text_statement_not_found(self):
        """
        Test that None is returned by the find method
        when a matching statement is not found.
        """
        results = list(self.adapter.filter(text="Non-existant"))
        self.assertEqual(len(results), 0)

    def test_filter_text_statement_found(self):
        """
        Test that a matching statement is returned
        when it exists in the database.
        """
        text = "New statement"
        self.adapter.create(text=text)
        results = list(self.adapter.filter(text=text))

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].text, text)

    def test_update_adds_new_statement(self):
        statement = Statement(text="New statement")
        self.adapter.update(statement)

        results = list(self.adapter.filter(text="New statement"))
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].text, statement.text)

    def test_update_modifies_existing_statement(self):
        statement = Statement(text="New statement")
        self.adapter.update(statement)

        # Check the initial values
        results = list(self.adapter.filter(text=statement.text))

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].in_response_to, None)

        # Update the statement value
        statement.in_response_to = "New response"
        self.adapter.update(statement)

        # Check that the values have changed
        results = list(self.adapter.filter(text=statement.text))

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].in_response_to, "New response")

    def test_get_random_returns_statement(self):
        self.adapter.create(text="New statement")

        random_statement = self.adapter.get_random()
        self.assertEqual(random_statement.text, "New statement")

    def test_get_random_no_data(self):
        from chatterbot.storage import StorageAdapter

        with self.assertRaises(StorageAdapter.EmptyDatabaseException):
            self.adapter.get_random()

    def test_remove(self):
        text = "Sometimes you have to run before you can walk."
        self.adapter.create(text=text)
        self.adapter.remove(text)
        results = self.adapter.filter(text=text)

        self.assertEqual(list(results), [])


class SQLStorageAdapterFilterTests(SQLStorageAdapterTestCase):

    def test_filter_text_no_matches(self):
        self.adapter.create(
            text='Testing...',
            in_response_to='Why are you counting?'
        )
        results = list(self.adapter.filter(text="Howdy"))

        self.assertEqual(len(results), 0)

    def test_filter_in_response_to_no_matches(self):
        self.adapter.create(
            text='Testing...',
            in_response_to='Why are you counting?'
        )

        results = list(self.adapter.filter(in_response_to="Maybe"))

        self.assertEqual(len(results), 0)

    def test_filter_equal_results(self):
        statement1 = Statement(
            text="Testing...",
            in_response_to=None
        )
        statement2 = Statement(
            text="Testing one, two, three.",
            in_response_to=None
        )
        self.adapter.update(statement1)
        self.adapter.update(statement2)

        results = list(self.adapter.filter(in_response_to=None))

        results_text = [
            result.text for result in results
        ]

        self.assertEqual(len(results), 2)
        self.assertIn(statement1.text, results_text)
        self.assertIn(statement2.text, results_text)

    def test_filter_no_parameters(self):
        """
        If no parameters are passed to the filter,
        then all statements should be returned.
        """
        self.adapter.create(text="Testing...")
        self.adapter.create(text="Testing one, two, three.")

        results = list(self.adapter.filter())

        self.assertEqual(len(results), 2)

    def test_filter_by_tag(self):
        self.adapter.create(text="Hello!", tags=["greeting", "salutation"])
        self.adapter.create(text="Hi everyone!", tags=["greeting", "exclamation"])
        self.adapter.create(text="The air contains Oxygen.", tags=["fact"])

        results = self.adapter.filter(tags=["greeting"])

        results_text_list = [statement.text for statement in results]

        self.assertEqual(len(results_text_list), 2)
        self.assertIn("Hello!", results_text_list)
        self.assertIn("Hi everyone!", results_text_list)

    def test_filter_by_tags(self):
        self.adapter.create(text="Hello!", tags=["greeting", "salutation"])
        self.adapter.create(text="Hi everyone!", tags=["greeting", "exclamation"])
        self.adapter.create(text="The air contains Oxygen.", tags=["fact"])

        results = self.adapter.filter(
            tags=["exclamation", "fact"]
        )

        results_text_list = [statement.text for statement in results]

        self.assertEqual(len(results_text_list), 2)
        self.assertIn("Hi everyone!", results_text_list)
        self.assertIn("The air contains Oxygen.", results_text_list)

    def test_filter_page_size(self):
        self.adapter.create(text='A')
        self.adapter.create(text='B')
        self.adapter.create(text='C')

        results = self.adapter.filter(page_size=2)

        results_text_list = [statement.text for statement in results]

        self.assertEqual(len(results_text_list), 3)
        self.assertIn('A', results_text_list)
        self.assertIn('B', results_text_list)
        self.assertIn('C', results_text_list)

    def test_exclude_text(self):
        self.adapter.create(text='Hello!')
        self.adapter.create(text='Hi everyone!')

        results = list(self.adapter.filter(
            exclude_text=[
                'Hello!'
            ]
        ))

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].text, 'Hi everyone!')

    def test_exclude_text_words(self):
        self.adapter.create(text='This is a good example.')
        self.adapter.create(text='This is a bad example.')
        self.adapter.create(text='This is a worse example.')

        results = list(self.adapter.filter(
            exclude_text_words=[
                'bad', 'worse'
            ]
        ))

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].text, 'This is a good example.')

    def test_persona_not_startswith(self):
        self.adapter.create(text='Hello!', persona='bot:tester')
        self.adapter.create(text='Hi everyone!', persona='user:person')

        results = list(self.adapter.filter(
            persona_not_startswith='bot:'
        ))

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].text, 'Hi everyone!')

    def test_search_text_contains(self):
        self.adapter.create(text='Hello!', search_text='hello exclamation')
        self.adapter.create(text='Hi everyone!', search_text='hi everyone')

        results = list(self.adapter.filter(
            search_text_contains='everyone'
        ))

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].text, 'Hi everyone!')

    def test_search_text_contains_multiple_matches(self):
        self.adapter.create(text='Hello!', search_text='hello exclamation')
        self.adapter.create(text='Hi everyone!', search_text='hi everyone')

        results = list(self.adapter.filter(
            search_text_contains='hello everyone'
        ))

        self.assertEqual(len(results), 2)


class SQLOrderingTests(SQLStorageAdapterTestCase):
    """
    Test cases for the ordering of sets of statements.
    """

    def test_order_by_text(self):
        statement_a = Statement(text='A is the first letter of the alphabet.')
        statement_b = Statement(text='B is the second letter of the alphabet.')

        self.adapter.update(statement_b)
        self.adapter.update(statement_a)

        results = list(self.adapter.filter(order_by=['text']))

        self.assertEqual(len(results), 2)
        self.assertEqual(statement_a.text, results[0].text)
        self.assertEqual(statement_b.text, results[1].text)

    def test_order_by_created_at(self):
        from datetime import datetime, timedelta

        today = datetime.now()
        yesterday = datetime.now() - timedelta(days=1)

        statement_a = Statement(
            text='A is the first letter of the alphabet.',
            created_at=yesterday
        )
        statement_b = Statement(
            text='B is the second letter of the alphabet.',
            created_at=today
        )

        self.adapter.update(statement_b)
        self.adapter.update(statement_a)

        results = list(self.adapter.filter(order_by=['created_at']))

        self.assertEqual(len(results), 2)
        self.assertEqual(statement_a.text, results[0].text)
        self.assertEqual(statement_b.text, results[1].text)


class StorageAdapterCreateTests(SQLStorageAdapterTestCase):
    """
    Tests for the create function of the storage adapter.
    """

    def test_create_text(self):
        self.adapter.create(text='testing')

        results = list(self.adapter.filter())

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].text, 'testing')

    def test_create_search_text(self):
        self.adapter.create(
            text='testing',
            search_text='test'
        )

        results = list(self.adapter.filter())

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].search_text, 'test')

    def test_create_search_in_response_to(self):
        self.adapter.create(
            text='testing',
            search_in_response_to='test'
        )

        results = list(self.adapter.filter())

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].search_in_response_to, 'test')

    def test_create_tags(self):
        self.adapter.create(text='testing', tags=['a', 'b'])

        results = list(self.adapter.filter())

        self.assertEqual(len(results), 1)
        self.assertIn('a', results[0].get_tags())
        self.assertIn('b', results[0].get_tags())

    def test_create_duplicate_tags(self):
        """
        The storage adapter should not create a statement with tags
        that are duplicates.
        """
        self.adapter.create(text='testing', tags=['ab', 'ab'])

        results = list(self.adapter.filter())

        self.assertEqual(len(results), 1)
        self.assertEqual(len(results[0].get_tags()), 1)
        self.assertEqual(results[0].get_tags(), ['ab'])

    def test_create_many_text(self):
        self.adapter.create_many([
            Statement(text='A'),
            Statement(text='B')
        ])

        results = list(self.adapter.filter())

        self.assertEqual(len(results), 2)
        self.assertEqual(results[0].text, 'A')
        self.assertEqual(results[1].text, 'B')

    def test_create_many_search_text(self):
        self.adapter.create_many([
            Statement(text='A', search_text='a'),
            Statement(text='B', search_text='b')
        ])

        results = list(self.adapter.filter())

        self.assertEqual(len(results), 2)
        self.assertEqual(results[0].search_text, 'a')
        self.assertEqual(results[1].search_text, 'b')

    def test_create_many_search_in_response_to(self):
        self.adapter.create_many([
            Statement(text='A', search_in_response_to='a'),
            Statement(text='B', search_in_response_to='b')
        ])

        results = list(self.adapter.filter())

        self.assertEqual(len(results), 2)
        self.assertEqual(results[0].search_in_response_to, 'a')
        self.assertEqual(results[1].search_in_response_to, 'b')

    def test_create_many_tags(self):
        self.adapter.create_many([
            Statement(text='A', tags=['first', 'letter']),
            Statement(text='B', tags=['second', 'letter'])
        ])
        results = list(self.adapter.filter())

        self.assertEqual(len(results), 2)
        self.assertIn('letter', results[0].get_tags())
        self.assertIn('letter', results[1].get_tags())
        self.assertIn('first', results[0].get_tags())
        self.assertIn('second', results[1].get_tags())

    def test_create_many_duplicate_tags(self):
        """
        The storage adapter should not create a statement with tags
        that are duplicates.
        """
        self.adapter.create_many([
            Statement(text='testing', tags=['ab', 'ab'])
        ])

        results = list(self.adapter.filter())

        self.assertEqual(len(results), 1)
        self.assertEqual(len(results[0].get_tags()), 1)
        self.assertEqual(results[0].get_tags(), ['ab'])


class StorageAdapterUpdateTests(SQLStorageAdapterTestCase):
    """
    Tests for the update function of the storage adapter.
    """

    def test_update_adds_tags(self):
        statement = self.adapter.create(text='Testing')
        statement.add_tags('a', 'b')
        self.adapter.update(statement)

        statements = list(self.adapter.filter())

        self.assertEqual(len(statements), 1)
        self.assertIn('a', statements[0].get_tags())
        self.assertIn('b', statements[0].get_tags())

    def test_update_duplicate_tags(self):
        """
        The storage adapter should not update a statement with tags
        that are duplicates.
        """
        statement = self.adapter.create(text='Testing', tags=['ab'])
        statement.add_tags('ab')
        self.adapter.update(statement)

        statements = list(self.adapter.filter())

        self.assertEqual(len(statements), 1)
        self.assertEqual(len(statements[0].get_tags()), 1)
        self.assertEqual(statements[0].get_tags(), ['ab'])
