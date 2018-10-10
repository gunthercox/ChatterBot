from unittest import TestCase
from chatterbot.storage import MongoDatabaseAdapter
from chatterbot.conversation import Statement


class MongoAdapterTestCase(TestCase):

    def setUp(self):
        """
        Instantiate the adapter.
        """
        from pymongo.errors import ServerSelectionTimeoutError
        from pymongo import MongoClient

        # Skip these tests if a mongo client is not running
        try:
            client = MongoClient(
                serverSelectionTimeoutMS=0.1
            )
            client.server_info()

            self.adapter = MongoDatabaseAdapter(
                database_uri="mongodb://localhost:27017/chatterbot_test_database"
            )

        except ServerSelectionTimeoutError:
            self.skipTest("Unable to connect to mongo database.")

    def tearDown(self):
        """
        Remove the test database.
        """
        self.adapter.drop()


class MongoDatabaseAdapterTestCase(MongoAdapterTestCase):

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
        statement = Statement(text="New statement")
        self.adapter.update(statement)

        results = self.adapter.filter(text="New statement")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].text, statement.text)

    def test_update_modifies_existing_statement(self):
        statement = Statement(text="New statement")
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
        text = "New statement"
        self.adapter.create(text=text)
        random_statement = self.adapter.get_random()

        self.assertEqual(random_statement.text, text)

    def test_mongo_to_object(self):
        self.adapter.create(text='Hello', in_response_to='Hi')
        statement_data = self.adapter.statements.find_one({'text': 'Hello'})

        obj = self.adapter.mongo_to_object(statement_data)

        self.assertEqual(type(obj), Statement)
        self.assertEqual(obj.text, 'Hello')
        self.assertEqual(obj.in_response_to, 'Hi')
        self.assertEqual(obj.id, statement_data['_id'])

    def test_remove(self):
        text = "Sometimes you have to run before you can walk."
        self.adapter.create(text=text)
        self.adapter.remove(text)
        results = self.adapter.filter(text=text)

        self.assertEqual(results, [])

    def test_remove_response(self):
        text = "Sometimes you have to run before you can walk."
        self.adapter.create(text='', in_response_to=text)
        self.adapter.remove(text)
        results = self.adapter.filter(text=text)

        self.assertEqual(results, [])

    def test_get_response_statements(self):
        """
        Test that we are able to get a list of only statements
        that are known to be in response to another statement.
        """
        self.adapter.create(text="What... is your quest?")
        self.adapter.create(text="This is a phone.")
        self.adapter.create(text="A what?", in_response_to="This is a phone.")
        self.adapter.create(text="A phone.", in_response_to="A what?")

        responses = list(self.adapter.get_response_statements())

        self.assertIn("This is a phone.", responses)
        self.assertIn("A what?", responses)
        self.assertEqual(len(responses), 2)

    def test_get_response_statements_bot_responses_filtered_out(self):
        """
        Responses generated by the chat bot should not be included in results.
        """
        self.adapter.create(text='Hello')
        self.adapter.create(text='Hi, how are you today?', in_response_to='Hello', persona='bot:Test')
        self.adapter.create(text='I am doing great.', in_response_to='Hi, how are you today?')
        self.adapter.create(text='That is awesome to hear.', in_response_to='I am doing great.', persona='bot:Test')
        self.adapter.create(text='Thank you.', in_response_to='That is awesome to hear.')

        responses = list(self.adapter.get_response_statements())

        self.assertIn('Hello', responses)
        self.assertIn('I am doing great.', responses)
        self.assertEqual(len(responses), 2)


class MongoAdapterFilterTestCase(MongoAdapterTestCase):

    def setUp(self):
        super(MongoAdapterFilterTestCase, self).setUp()

        self.statement1 = Statement(
            text="Testing...",
            in_response_to="Why are you counting?"
        )
        self.statement2 = Statement(
            text="Testing one, two, three.",
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
            text="Testing...",
            in_response_to=[]
        )
        statement2 = Statement(
            text="Testing one, two, three.",
            in_response_to=[]
        )
        self.adapter.update(statement1)
        self.adapter.update(statement2)

        results = self.adapter.filter(in_response_to=[])
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

    def test_filter_in_response_to(self):
        self.adapter.create(text="A", in_response_to="Yes")
        self.adapter.create(text="B", in_response_to="No")

        results = self.adapter.filter(
            in_response_to="Yes"
        )

        # Get the first response
        response = results[0]

        self.assertEqual(len(results), 1)
        self.assertEqual(response.in_response_to, "Yes")

    def test_filter_by_tag(self):
        self.adapter.create(text="Hello!", tags=["greeting", "salutation"])
        self.adapter.create(text="Hi everyone!", tags=["greeting", "exclamation"])
        self.adapter.create(text="The air contains Oxygen.", tags=["fact"])

        results = self.adapter.filter(tags="greeting")

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


class MongoOrderingTestCase(MongoAdapterTestCase):
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
            created_at=today
        )
        statement_b = Statement(
            text='B is the second letter of the alphabet.',
            created_at=yesterday
        )

        self.adapter.update(statement_b)
        self.adapter.update(statement_a)

        results = self.adapter.filter(order_by=['created_at'])

        self.assertEqual(len(results), 2)
        self.assertEqual(results[0], statement_a)
        self.assertEqual(results[1], statement_b)


class StorageAdapterCreateTestCase(MongoAdapterTestCase):
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

    def test_create_duplicate_tags(self):
        """
        The storage adapter should not create a statement with tags
        that are duplicates.
        """
        self.adapter.create(text='testing', tags=['ab', 'ab'])

        results = self.adapter.filter()

        self.assertEqual(len(results), 1)
        self.assertEqual(len(results[0].get_tags()), 1)
        self.assertEqual(results[0].get_tags(), ['ab'])

    def test_create_many_text(self):
        self.adapter.create_many([
            {
                'text': 'A'
            },
            {
                'text': 'B'
            }
        ])

        results = self.adapter.filter()

        self.assertEqual(len(results), 2)
        self.assertEqual(results[0].text, 'A')
        self.assertEqual(results[1].text, 'B')

    def test_create_many_tags(self):
        self.adapter.create_many([
            {
                'text': 'A',
                'tags': ['first', 'letter']
            },
            {
                'text': 'B',
                'tags': ['second', 'letter']
            }
        ])
        results = self.adapter.filter()

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
            {
                'text': 'testing',
                'tags': ['ab', 'ab']
            }
        ])

        results = self.adapter.filter()

        self.assertEqual(len(results), 1)
        self.assertEqual(len(results[0].get_tags()), 1)
        self.assertEqual(results[0].get_tags(), ['ab'])


class StorageAdapterUpdateTestCase(MongoAdapterFilterTestCase):
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

    def test_update_duplicate_tags(self):
        """
        The storage adapter should not update a statement with tags
        that are duplicates.
        """
        statement = self.adapter.create(text='Testing', tags=['ab'])
        statement.add_tags('ab')
        self.adapter.update(statement)

        statements = self.adapter.filter()

        self.assertEqual(len(statements), 1)
        self.assertEqual(len(statements[0].get_tags()), 1)
        self.assertEqual(statements[0].get_tags(), ['ab'])
