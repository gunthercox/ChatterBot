from unittest import TestCase
from chatterbot.conversation import Statement
from chatterbot.storage.sql_storage import SQLStorageAdapter


class SQLAlchemyAdapterTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        """
        Instantiate the adapter before any tests in the test case run.
        """
        cls.adapter = SQLStorageAdapter()

    def setUp(self):
        """
        Create the tables in the database before each test is run.
        """
        self.adapter.create_database()

    def tearDown(self):
        """
        Drop the tables in the database after each test is run.
        """
        self.adapter.drop()


class SQLStorageAdapterTestCase(SQLAlchemyAdapterTestCase):

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
        self.assertEqual(len(self.adapter.filter(text="Non-existant")), 0)

    def test_filter_text_statement_found(self):
        """
        Test that a matching statement is returned
        when it exists in the database.
        """
        text = "New statement"
        self.adapter.create(text=text)
        results = self.adapter.filter(text=text)

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].text, text)

    def test_update_adds_new_statement(self):
        statement = Statement("New statement")
        self.adapter.update(statement)

        results = self.adapter.filter(text="New statement")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].text, statement.text)

    def test_update_modifies_existing_statement(self):
        statement = Statement("New statement")
        self.adapter.update(statement)

        # Check the initial values
        results = self.adapter.filter(text=statement.text)

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].in_response_to, None)

        # Update the statement value
        statement.in_response_to = "New response"
        self.adapter.update(statement)

        # Check that the values have changed
        results = self.adapter.filter(text=statement.text)

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].in_response_to, "New response")

    def test_get_random_returns_statement(self):
        self.adapter.create(text="New statement")

        random_statement = self.adapter.get_random()
        self.assertEqual(random_statement.text, "New statement")

    def test_remove(self):
        text = "Sometimes you have to run before you can walk."
        self.adapter.create(text=text)
        self.adapter.remove(text)
        results = self.adapter.filter(text=text)

        self.assertEqual(results, [])

    def test_get_response_statements(self):
        """
        Test that we are able to get a list of only statements
        that are known to be in response to another statement.
        """
        statement_list = [
            Statement("What... is your quest?"),
            Statement("This is a phone."),
            Statement("A what?", in_response_to="This is a phone."),
            Statement("A phone.", in_response_to="A what?")
        ]

        for statement in statement_list:
            self.adapter.update(statement)

        responses = self.adapter.get_response_statements()

        self.assertEqual(len(responses), 2)
        self.assertIn("This is a phone.", responses)
        self.assertIn("A what?", responses)


class SQLAlchemyStorageAdapterFilterTestCase(SQLAlchemyAdapterTestCase):

    def setUp(self):
        super(SQLAlchemyStorageAdapterFilterTestCase, self).setUp()

        self.statement1 = Statement(
            "Testing...",
            in_response_to="Why are you counting?"
        )
        self.statement2 = Statement(
            "Testing one, two, three.",
            in_response_to="Testing..."
        )

    def test_filter_text_no_matches(self):
        self.adapter.update(self.statement1)
        results = self.adapter.filter(text="Howdy")

        self.assertEqual(len(results), 0)

    def test_filter_in_response_to_no_matches(self):
        self.adapter.update(self.statement1)

        results = self.adapter.filter(in_response_to="Maybe")
        self.assertEqual(len(results), 0)

    def test_filter_equal_results(self):
        statement1 = Statement(
            "Testing...",
            in_response_to=None
        )
        statement2 = Statement(
            "Testing one, two, three.",
            in_response_to=None
        )
        self.adapter.update(statement1)
        self.adapter.update(statement2)

        results = self.adapter.filter(in_response_to=None)
        self.assertEqual(len(results), 2)
        self.assertIn(statement1, results)
        self.assertIn(statement2, results)

    def test_filter_no_parameters(self):
        """
        If no parameters are passed to the filter,
        then all statements should be returned.
        """
        self.adapter.create(text="Testing...")
        self.adapter.create(text="Testing one, two, three.")

        results = self.adapter.filter()

        self.assertEqual(len(results), 2)

    def test_response_list_in_results(self):
        """
        If a statement with response values is found using
        the filter method, they should be returned as
        response objects.
        """
        statement = Statement(
            "The first is to help yourself, the second is to help others.",
            in_response_to="Why do people have two hands?"
        )
        self.adapter.update(statement)
        found = self.adapter.filter(text=statement.text)

        self.assertEqual(found[0].in_response_to, statement.in_response_to)


class ReadOnlySQLStorageAdapterTestCase(SQLAlchemyAdapterTestCase):

    def setUp(self):
        """
        Make the adapter writable before every test.
        """
        super(ReadOnlySQLStorageAdapterTestCase, self).setUp()
        self.adapter.read_only = False

    def test_update_does_not_add_new_statement(self):
        self.adapter.read_only = True

        statement = Statement("New statement")
        self.adapter.update(statement)

        results = self.adapter.filter(text="New statement")
        self.assertEqual(len(results), 0)

    def test_update_does_not_modify_existing_statement(self):
        statement = Statement("New statement")
        self.adapter.update(statement)

        self.adapter.read_only = True

        statement.in_response_to = "New statement"
        self.adapter.update(statement)

        results = self.adapter.filter(text="New statement")

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].text, statement.text)
        self.assertEqual(results[0].in_response_to, None)


class SQLOrderingTestCase(SQLAlchemyAdapterTestCase):
    """
    Test cases for the ordering of sets of statements.
    """

    def test_order_by_text(self):
        statement_a = Statement(text='A is the first letter of the alphabet.')
        statement_b = Statement(text='B is the second letter of the alphabet.')

        self.adapter.update(statement_b)
        self.adapter.update(statement_a)

        results = self.adapter.filter(order_by=['text'])

        self.assertEqual(len(results), 2)
        self.assertEqual(results[0], statement_a)
        self.assertEqual(results[1], statement_b)

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

        results = self.adapter.filter(order_by=['created_at'])

        self.assertEqual(len(results), 2)
        self.assertEqual(results[0], statement_a)
        self.assertEqual(results[1], statement_b)


class StorageAdapterCreateTestCase(SQLAlchemyAdapterTestCase):
    """
    Tests for the create function of the storage adapter.
    """

    def test_create_text(self):
        self.adapter.create(text='testing')

        results = self.adapter.filter()

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].text, 'testing')

    def test_create_tags(self):
        self.adapter.create(text='testing', tags=['a', 'b'])

        results = self.adapter.filter()

        self.assertEqual(len(results), 1)
        self.assertIn('a', results[0].get_tags())
        self.assertIn('b', results[0].get_tags())


class StorageAdapterUpdateTestCase(SQLAlchemyAdapterTestCase):
    """
    Tests for the update function of the storage adapter.
    """

    def test_update_adds_tags(self):
        statement = self.adapter.create(text='Testing')
        statement.add_tags('a', 'b')
        self.adapter.update(statement)

        statements = self.adapter.filter()

        self.assertEqual(len(statements), 1)
        self.assertIn('a', statements[0].get_tags())
        self.assertIn('b', statements[0].get_tags())
