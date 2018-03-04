from unittest import TestCase
from chatterbot.conversation import Statement, Response
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
        self.adapter.create()

    def tearDown(self):
        """
        Drop the tables in the database after each test is run.
        """
        self.adapter.drop()


class SQLStorageAdapterTestCase(SQLAlchemyAdapterTestCase):

    def test_get_latest_response_from_invalid_conversation_id(self):
        response = self.adapter.get_latest_response(0)

        self.assertIsNone(response)

    def test_get_latest_response_from_zero_responses(self):
        conversation_id = self.adapter.create_conversation()
        response = self.adapter.get_latest_response(conversation_id)

        self.assertIsNone(response)

    def test_get_latest_response_from_one_responses(self):
        conversation_id = self.adapter.create_conversation()
        statement_1 = Statement(text='A')
        statement_2 = Statement(text='B', in_response_to=[Response(text=statement_1.text)])

        self.adapter.add_to_conversation(conversation_id, statement_1, statement_2)

        response = self.adapter.get_latest_response(conversation_id)

        self.assertEqual(statement_1, response)

    def test_get_latest_response_from_two_responses(self):
        conversation_id = self.adapter.create_conversation()
        statement_1 = Statement(text='A')
        statement_2 = Statement(text='B', in_response_to=[Response(text=statement_1.text)])
        statement_3 = Statement(text='C', in_response_to=[Response(text=statement_2.text)])

        self.adapter.add_to_conversation(conversation_id, statement_1, statement_2)
        self.adapter.add_to_conversation(conversation_id, statement_2, statement_3)

        response = self.adapter.get_latest_response(conversation_id)

        self.assertEqual(statement_2, response)

    def test_get_latest_response_from_three_responses(self):
        conversation_id = self.adapter.create_conversation()
        statement_1 = Statement(text='A')
        statement_2 = Statement(text='B', in_response_to=[Response(text=statement_1.text)])
        statement_3 = Statement(text='C', in_response_to=[Response(text=statement_2.text)])
        statement_4 = Statement(text='D', in_response_to=[Response(text=statement_3.text)])

        self.adapter.add_to_conversation(conversation_id, statement_1, statement_2)
        self.adapter.add_to_conversation(conversation_id, statement_2, statement_3)
        self.adapter.add_to_conversation(conversation_id, statement_3, statement_4)

        response = self.adapter.get_latest_response(conversation_id)

        self.assertEqual(statement_3, response)

    def test_set_database_name_none(self):
        adapter = SQLStorageAdapter(database=None)
        self.assertEqual(adapter.database_uri, 'sqlite://')

    def test_set_database_name(self):
        adapter = SQLStorageAdapter(database='test.sqlite3')
        self.assertEqual(adapter.database_uri, 'sqlite:///test.sqlite3')

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
        statement = Statement("Test statement")
        self.adapter.update(statement)
        self.assertEqual(self.adapter.count(), 1)

    def test_statement_not_found(self):
        """
        Test that None is returned by the find method
        when a matching statement is not found.
        """
        self.assertIsNone(self.adapter.find("Non-existant"))

    def test_statement_found(self):
        """
        Test that a matching statement is returned
        when it exists in the database.
        """
        statement = Statement("New statement")
        self.adapter.update(statement)

        found_statement = self.adapter.find("New statement")
        self.assertIsNotNone(found_statement)
        self.assertEqual(found_statement.text, statement.text)

    def test_update_adds_new_statement(self):
        statement = Statement("New statement")
        self.adapter.update(statement)

        statement_found = self.adapter.find("New statement")
        self.assertIsNotNone(statement_found)
        self.assertEqual(statement_found.text, statement.text)

    def test_update_modifies_existing_statement(self):
        statement = Statement("New statement")
        self.adapter.update(statement)

        # Check the initial values
        found_statement = self.adapter.find(statement.text)
        self.assertEqual(
            len(found_statement.in_response_to), 0
        )

        # Update the statement value
        statement.add_response(
            Response("New response")
        )
        self.adapter.update(statement)

        # Check that the values have changed
        found_statement = self.adapter.find(statement.text)
        self.assertEqual(
            len(found_statement.in_response_to), 1
        )

    def test_get_random_returns_statement(self):
        statement = Statement("New statement")
        self.adapter.update(statement)

        random_statement = self.adapter.get_random()
        self.assertEqual(random_statement.text, statement.text)

    def test_find_returns_nested_responses(self):
        response_list = [
            Response("Yes"),
            Response("No")
        ]
        statement = Statement(
            "Do you like this?",
            in_response_to=response_list
        )
        self.adapter.update(statement)

        result = self.adapter.find(statement.text)

        self.assertIn("Yes", result.in_response_to)
        self.assertIn("No", result.in_response_to)

    def test_multiple_responses_added_on_update(self):
        statement = Statement(
            "You are welcome.",
            in_response_to=[
                Response("Thank you."),
                Response("Thanks.")
            ]
        )
        self.adapter.update(statement)
        result = self.adapter.find(statement.text)

        self.assertEqual(len(result.in_response_to), 2)
        self.assertIn(statement.in_response_to[0], result.in_response_to)
        self.assertIn(statement.in_response_to[1], result.in_response_to)

    def test_update_saves_statement_with_multiple_responses(self):
        statement = Statement(
            "You are welcome.",
            in_response_to=[
                Response("Thank you."),
                Response("Thanks."),
            ]
        )
        self.adapter.update(statement)
        response = self.adapter.find(statement.text)

        self.assertEqual(len(response.in_response_to), 2)

    def test_getting_and_updating_statement(self):
        statement = Statement("Hi")
        self.adapter.update(statement)

        statement.add_response(Response("Hello"))
        statement.add_response(Response("Hello"))
        self.adapter.update(statement)

        response = self.adapter.find(statement.text)

        self.assertEqual(len(response.in_response_to), 1)
        self.assertEqual(response.in_response_to[0].occurrence, 2)

    def test_remove(self):
        text = "Sometimes you have to run before you can walk."
        statement = Statement(text)
        self.adapter.update(statement)
        self.adapter.remove(statement.text)
        result = self.adapter.find(text)

        self.assertIsNone(result)

    def test_remove_response(self):
        text = "Sometimes you have to run before you can walk."
        statement = Statement(
            "A test flight is not recommended at this design phase.",
            in_response_to=[Response(text)]
        )
        self.adapter.update(statement)
        self.adapter.remove(statement.text)
        results = self.adapter.filter(in_response_to__contains=text)

        self.assertEqual(results, [])

    def test_get_response_statements(self):
        """
        Test that we are able to get a list of only statements
        that are known to be in response to another statement.
        """
        statement_list = [
            Statement("What... is your quest?"),
            Statement("This is a phone."),
            Statement("A what?", in_response_to=[Response("This is a phone.")]),
            Statement("A phone.", in_response_to=[Response("A what?")])
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
            in_response_to=[
                Response("Why are you counting?")
            ]
        )
        self.statement2 = Statement(
            "Testing one, two, three.",
            in_response_to=[
                Response("Testing...")
            ]
        )

    def test_filter_text_no_matches(self):
        self.adapter.update(self.statement1)
        results = self.adapter.filter(text="Howdy")

        self.assertEqual(len(results), 0)

    def test_filter_in_response_to_no_matches(self):
        self.adapter.update(self.statement1)

        results = self.adapter.filter(
            in_response_to=[Response("Maybe")]
        )
        self.assertEqual(len(results), 0)

    def test_filter_equal_results(self):
        statement1 = Statement(
            "Testing...",
            in_response_to=[]
        )
        statement2 = Statement(
            "Testing one, two, three.",
            in_response_to=[]
        )
        self.adapter.update(statement1)
        self.adapter.update(statement2)

        results = self.adapter.filter(in_response_to=[])
        self.assertEqual(len(results), 2)
        self.assertIn(statement1, results)
        self.assertIn(statement2, results)

    def test_filter_contains_result(self):
        self.adapter.update(self.statement1)
        self.adapter.update(self.statement2)

        results = self.adapter.filter(
            in_response_to__contains="Why are you counting?"
        )
        self.assertEqual(len(results), 1)
        self.assertIn(self.statement1, results)

    def test_filter_contains_no_result(self):
        self.adapter.update(self.statement1)

        results = self.adapter.filter(
            in_response_to__contains="How do you do?"
        )
        self.assertEqual(results, [])

    def test_filter_multiple_parameters(self):
        self.adapter.update(self.statement1)
        self.adapter.update(self.statement2)

        results = self.adapter.filter(
            text="Testing...",
            in_response_to__contains="Why are you counting?"
        )

        self.assertEqual(len(results), 1)
        self.assertIn(self.statement1, results)

    def test_filter_multiple_parameters_no_results(self):
        self.adapter.update(self.statement1)
        self.adapter.update(self.statement2)

        results = self.adapter.filter(
            text="Test",
            in_response_to__contains="Not an existing response."
        )

        self.assertEqual(len(results), 0)

    def test_filter_no_parameters(self):
        """
        If no parameters are passed to the filter,
        then all statements should be returned.
        """
        statement1 = Statement("Testing...")
        statement2 = Statement("Testing one, two, three.")
        self.adapter.update(statement1)
        self.adapter.update(statement2)

        results = self.adapter.filter()

        self.assertEqual(len(results), 2)

    def test_filter_returns_statement_with_multiple_responses(self):
        statement = Statement(
            "You are welcome.",
            in_response_to=[
                Response("Thanks."),
                Response("Thank you.")
            ]
        )
        self.adapter.update(statement)
        response = self.adapter.filter(
            in_response_to__contains="Thanks."
        )

        # Get the first response
        response = response[0]

        self.assertEqual(len(response.in_response_to), 2)

    def test_response_list_in_results(self):
        """
        If a statement with response values is found using
        the filter method, they should be returned as
        response objects.
        """
        statement = Statement(
            "The first is to help yourself, the second is to help others.",
            in_response_to=[
                Response("Why do people have two hands?")
            ]
        )
        self.adapter.update(statement)
        found = self.adapter.filter(text=statement.text)

        self.assertEqual(len(found[0].in_response_to), 1)
        self.assertIsInstance(found[0].in_response_to[0], Response)


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

        statement_found = self.adapter.find("New statement")
        self.assertIsNone(statement_found)

    def test_update_does_not_modify_existing_statement(self):
        statement = Statement("New statement")
        self.adapter.update(statement)

        self.adapter.read_only = True

        statement.add_response(
            Response("New response")
        )

        self.adapter.update(statement)

        statement_found = self.adapter.find("New statement")
        self.assertEqual(statement_found.text, statement.text)
        self.assertEqual(
            len(statement_found.in_response_to), 0
        )
