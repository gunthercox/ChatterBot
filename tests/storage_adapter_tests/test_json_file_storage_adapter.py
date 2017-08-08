from unittest import TestCase
from chatterbot.storage import JsonFileStorageAdapter
from chatterbot.conversation import Statement, Response


class JsonAdapterTestCase(TestCase):

    def setUp(self):
        """
        Instantiate the adapter.
        """
        from random import randint

        # Generate a random name for the database
        database_name = str(randint(0, 9000))

        self.adapter = JsonFileStorageAdapter(
            database=database_name,
            silence_performance_warning=True
        )

    def tearDown(self):
        """
        Remove the test database.
        """
        self.adapter.drop()


class JsonFileStorageAdapterTestCase(JsonAdapterTestCase):

    def test_json_to_object(self):
        data = {
            'text': 'Test statement',
            'in_response_to': [
                {'text': 'Test response'}
            ]
        }
        obj = self.adapter.json_to_object(data)

        self.assertEqual(obj.text, data['text'])
        self.assertEqual(len(obj.in_response_to), 1)
        self.assertEqual(obj.in_response_to[0].text, data['in_response_to'][0]['text'])

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

    def test_deserialize_responses(self):
        response_list = [
            {"text": "Test", "occurrence": 3},
            {"text": "Testing", "occurrence": 1},
        ]
        results = self.adapter.deserialize_responses(response_list)

        self.assertEqual(len(results), 2)

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


class JsonFileStorageAdapterFilterTestCase(JsonAdapterTestCase):

    def setUp(self):
        super(JsonFileStorageAdapterFilterTestCase, self).setUp()

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
            in_response_to="Maybe"
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
        self.assertEqual(type(found[0].in_response_to[0]), Response)


class JsonFileStorageOrderingTestCase(JsonAdapterTestCase):
    """
    Test cases for the ordering of sets of statements.
    """

    def test_order_by_text(self):
        statement_a = Statement(text='A is the first letter of the alphabet.')
        statement_b = Statement(text='B is the second letter of the alphabet.')

        self.adapter.update(statement_a)
        self.adapter.update(statement_b)

        results = self.adapter.filter(order_by='text')

        self.assertEqual(len(results), 2)
        self.assertEqual(results[0], statement_a)
        self.assertEqual(results[1], statement_b)
