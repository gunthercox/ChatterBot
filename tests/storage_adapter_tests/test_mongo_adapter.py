from unittest import TestCase
from chatterbot.adapters.storage import MongoDatabaseAdapter
from chatterbot.conversation import Statement


class BaseMongoDatabaseAdapterTestCase(TestCase):

    def setUp(self):
        """
        Instantiate the adapter.
        """
        database_name = "test_db"

        self.adapter = MongoDatabaseAdapter(database=database_name)

    def tearDown(self):
        """
        Remove the test database.
        """
        self.adapter.drop()

class JsonDatabaseAdapterTestCase(BaseMongoDatabaseAdapterTestCase):

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


    def test_filter_no_results(self):
        statement1 = Statement(
            "Testing...",
            occurrence=4
        )
        self.adapter.update(statement1)

        results = self.adapter.filter(occurrence=100)
        self.assertEqual(len(results), 0)

    def test_filter_equal_result(self):
        statement1 = Statement(
            "Testing...",
            occurrence=22
        )
        statement2 = Statement(
            "Testing one, two, three.",
            occurrence=1
        )
        self.adapter.update(statement1)
        self.adapter.update(statement2)

        results = self.adapter.filter(occurrence=22)
        self.assertEqual(len(results), 1)
        self.assertIn(statement1, results)

    def test_filter_equal_multiple_results(self):
        statement1 = Statement(
            "Testing...",
            occurrence=6
        )
        statement2 = Statement(
            "Testing one, two, three.",
            occurrence=1
        )
        statement3 = Statement(
            "Test statement.",
            occurrence=6
        )
        self.adapter.update(statement1)
        self.adapter.update(statement2)
        self.adapter.update(statement3)

        results = self.adapter.filter(occurrence=6)
        self.assertEqual(len(results), 2)
        self.assertIn(statement1, results)
        self.assertIn(statement3, results)

    def test_filter_contains_result(self):
        statement1 = Statement(
            "Testing...",
            in_response_to=[
                "What are you doing?"
            ]
        )
        statement2 = Statement(
            "Testing one, two, three.",
            in_response_to=[
                "Testing..."
            ]
        )
        self.adapter.update(statement1)
        self.adapter.update(statement2)

        results = self.adapter.filter(
            in_response_to__contains="What are you doing?"
        )
        self.assertEqual(len(results), 1)
        self.assertIn(statement1, results)

    def test_filter_contains_no_result(self):
        statement1 = Statement(
            "Testing...",
            in_response_to=[
                "What are you doing?"
            ]
        )
        self.adapter.update(statement1)

        results = self.adapter.filter(
            in_response_to__contains="How do you do?"
        )
        self.assertEqual(len(results), 0)

    def test_filter_multiple_parameters(self):
        statement1 = Statement(
            "Testing...",
            occurrence=6,
            in_response_to=[
                "Why are you counting?"
            ]
        )
        statement2 = Statement(
            "Testing one, two, three.",
            occurrence=6,
            in_response_to=[
                "Testing..."
            ]
        )
        self.adapter.update(statement1)
        self.adapter.update(statement2)

        results = self.adapter.filter(
            occurrence=6,
            in_response_to__contains="Why are you counting?"
        )

        self.assertEqual(len(results), 1)
        self.assertIn(statement1, results)

    def test_filter_multiple_parameters_no_results(self):
        statement1 = Statement(
            "Testing...",
            occurrence=6,
            in_response_to=[
                "Why are you counting?"
            ]
        )
        statement2 = Statement(
            "Testing one, two, three.",
            occurrence=1,
            in_response_to=[
                "Testing..."
            ]
        )
        self.adapter.update(statement1)
        self.adapter.update(statement2)

        results = self.adapter.filter(
            occurrence=6,
            in_response_to__contains="Testing..."
        )

        self.assertEqual(len(results), 0)

    def test_filter_no_parameters(self):
        """
        If not parameters are provided to the filter,
        then all statements should be returned.
        """
        statement1 = Statement("Testing...")
        statement2 = Statement("Testing one, two, three.")
        self.adapter.update(statement1)
        self.adapter.update(statement2)

        results = self.adapter.filter()

        self.assertEqual(len(results), 2)


class ReadOnlyMongoDatabaseAdapterTestCase(BaseMongoDatabaseAdapterTestCase):

    def test_update_does_not_add_new_statement(self):
        self.adapter.read_only = True

        statement = Statement("New statement")
        self.adapter.update(statement)

        statement_found = self.adapter.find("New statement")
        self.assertEqual(statement_found, None)

    def test_update_does_not_modify_existing_statement(self):
        statement = Statement("New statement")
        self.adapter.update(statement)

        self.adapter.read_only = True

        statement.update_occurrence_count()
        self.adapter.update(statement)

        statement_found = self.adapter.find("New statement")
        self.assertEqual(statement_found.text, statement.text)
        self.assertEqual(statement.occurrence, 2)
        self.assertEqual(statement_found.occurrence, 1)

