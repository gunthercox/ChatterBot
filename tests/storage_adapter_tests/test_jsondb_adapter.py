from unittest import TestCase
from chatterbot.adapters.storage import JsonDatabaseAdapter
from chatterbot.conversation import Statement


class BaseJsonDatabaseAdapterTestCase(TestCase):

    def setUp(self):
        """
        Instantiate the adapter.
        """
        from random import randint

        # Generate a random name for the database
        database_name = str(randint(0, 9000))

        self.adapter = JsonDatabaseAdapter(database=database_name)

    def tearDown(self):
        """
        Remove the test database.
        """
        self.adapter.drop()


class JsonDatabaseAdapterTestCase(BaseJsonDatabaseAdapterTestCase):

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
        statement = Statement("Test statement")
        self.adapter.update(statement)
        self.assertEqual(self.adapter.count(), 1)

    def test_statement_not_found(self):
        """
        Test that None is returned by the find method
        when a matching statement is not found.
        """
        self.assertEqual(self.adapter.find("Non-existant"), None)

    def test_statement_found(self):
        """
        Test that a matching statement is returned
        when it exists in the database.
        """
        statement = Statement("New statement")
        self.adapter.update(statement)

        found_statement = self.adapter.find("New statement")
        self.assertNotEqual(found_statement, None)
        self.assertEqual(found_statement.text, statement.text)

    def test_update_adds_new_statement(self):
        statement = Statement("New statement")
        self.adapter.update(statement)

        statement_found = self.adapter.find("New statement")
        self.assertNotEqual(statement_found, None)
        self.assertEqual(statement_found.text, statement.text)

    def test_update_modifies_existing_statement(self):
        statement = Statement("New statement")
        self.adapter.update(statement)

        # Check the initial values
        found_statement = self.adapter.find(statement.text)
        self.assertEqual(found_statement.occurrence, 1)

        # Update the statement value
        statement.update_occurrence_count()
        self.adapter.update(statement)

        # CHeck that the values have changed
        found_statement = self.adapter.find(statement.text)
        self.assertEqual(found_statement.occurrence, 2)

    def test_get_random_returns_statement(self):
        statement = Statement("New statement")
        self.adapter.update(statement)

        random_statement = self.adapter.get_random()
        self.assertEqual(random_statement.text, statement.text)

    def test_find_returns_nested_responces(self):
        response_list = [
            "Yes", "No"
        ]
        statement = Statement(
            "Do you like this?",
            in_response_to=response_list
        )
        self.adapter.update(statement)

        result = self.adapter.find(statement.text)

        self.assertIn("Yes", result.in_response_to)
        self.assertIn("No", result.in_response_to)


class ReadOnlyJsonDatabaseAdapterTestCase(BaseJsonDatabaseAdapterTestCase):
    pass

