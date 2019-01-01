from django.test import TestCase
from chatterbot.storage import DjangoStorageAdapter
from chatterbot.conversation import Statement as StatementObject
from chatterbot.ext.django_chatterbot.models import Statement


class DjangoAdapterTestCase(TestCase):

    def setUp(self):
        """
        Instantiate the adapter.
        """
        self.adapter = DjangoStorageAdapter()

    def tearDown(self):
        """
        Remove the test database.
        """
        self.adapter.drop()


class DjangoStorageAdapterTests(DjangoAdapterTestCase):

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

    def test_filter_statement_not_found(self):
        """
        Test that None is returned by the find method
        when a matching statement is not found.
        """
        results = list(self.adapter.filter(text="Non-existant"))
        self.assertEqual(len(results), 0)

    def test_filter_statement_found(self):
        """
        Test that a matching statement is returned
        when it exists in the database.
        """
        statement = self.adapter.create(text="New statement")

        results = list(self.adapter.filter(text="New statement"))

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].text, statement.text)

    def test_update_adds_new_statement(self):
        statement = Statement(text="New statement")
        self.adapter.update(statement)

        results = list(self.adapter.filter(text="New statement"))

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].text, statement.text)

    def test_update_modifies_existing_statement(self):
        statement = self.adapter.create(text="New statement")
        other_statement = self.adapter.create(text="New response")

        # Check the initial values
        results = list(self.adapter.filter(text=statement.text))

        self.assertEqual(results[0].in_response_to, None)

        statement.in_response_to = other_statement.text

        # Update the statement value
        self.adapter.update(statement)

        # Check that the values have changed
        results = list(self.adapter.filter(text=statement.text))

        self.assertEqual(results[0].in_response_to, other_statement.text)

    def test_get_random_returns_statement(self):
        statement = self.adapter.create(text="New statement")

        random_statement = self.adapter.get_random()
        self.assertEqual(random_statement.text, statement.text)

    def test_get_random_no_data(self):
        from chatterbot.storage import StorageAdapter

        with self.assertRaises(StorageAdapter.EmptyDatabaseException):
            self.adapter.get_random()

    def test_filter_by_text_multiple_results(self):
        self.adapter.create(
            text="Do you like this?",
            in_response_to="Yes"
        )
        self.adapter.create(
            text="Do you like this?",
            in_response_to="No"
        )

        results = list(self.adapter.filter(text="Do you like this?"))

        self.assertEqual(len(results), 2)

    def test_remove(self):
        text = "Sometimes you have to run before you can walk."
        statement = self.adapter.create(text=text)

        self.adapter.remove(statement.text)
        results = list(self.adapter.filter(text=text))

        self.assertEqual(len(results), 0)

    def test_remove_response(self):
        text = "Sometimes you have to run before you can walk."
        statement = self.adapter.create(text=text)
        self.adapter.remove(statement.text)
        results = list(self.adapter.filter(text=text))

        self.assertEqual(len(results), 0)


class DjangoAdapterFilterTests(DjangoAdapterTestCase):

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
        statement1 = self.adapter.create(text="Testing...")
        statement2 = self.adapter.create(text="Testing one, two, three.")

        results = list(self.adapter.filter(in_response_to=None))

        self.assertEqual(len(results), 2)

        text_for_statements = [
            statement.text for statement in results
        ]
        self.assertIn(statement1.text, text_for_statements)
        self.assertIn(statement2.text, text_for_statements)

    def test_filter_contains_result(self):
        self.adapter.create(
            text='Testing...',
            in_response_to='Why are you counting?'
        )
        self.adapter.create(
            text='Testing one, two, three.',
            in_response_to='Testing...'
        )

        results = list(self.adapter.filter(
            in_response_to="Why are you counting?"
        ))
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].text, 'Testing...')

    def test_filter_contains_no_result(self):
        self.adapter.create(
            text='Testing...',
            in_response_to='Why are you counting?'
        )

        results = list(self.adapter.filter(
            in_response_to="How do you do?"
        ))
        self.assertEqual(len(results), 0)

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

        results = list(self.adapter.filter(tags=["greeting"]))

        results_text_list = [statement.text for statement in results]

        self.assertEqual(len(results_text_list), 2)
        self.assertIn("Hello!", results_text_list)
        self.assertIn("Hi everyone!", results_text_list)

    def test_filter_by_tags(self):
        self.adapter.create(text="Hello!", tags=["greeting", "salutation"])
        self.adapter.create(text="Hi everyone!", tags=["greeting", "exclamation"])
        self.adapter.create(text="The air contains Oxygen.", tags=["fact"])

        results = list(self.adapter.filter(
            tags=["exclamation", "fact"]
        ))

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

    def test_confidence(self):
        """
        Test that the confidence value is not saved to the database.
        The confidence attribute on statements is intended to just hold
        the confidence of the statement when it returned as a response to
        some input. Because of that, the value of the confidence score
        should never be stored in the database with the statement.
        """
        statement = self.adapter.create(text='Test statement')
        statement.confidence = 0.5

        statement_updated = Statement.objects.get(pk=statement.id)

        self.assertEqual(statement_updated.confidence, 0)

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


class DjangoOrderingTests(DjangoAdapterTestCase):
    """
    Test cases for the ordering of sets of statements.
    """

    def test_order_by_text(self):
        statement_a = self.adapter.create(text='A is the first letter of the alphabet.')
        statement_b = self.adapter.create(text='B is the second letter of the alphabet.')

        results = list(self.adapter.filter(order_by=['text']))

        self.assertEqual(len(results), 2)
        self.assertEqual(results[0], statement_a)
        self.assertEqual(results[1], statement_b)

    def test_reverse_order_by_text(self):
        statement_a = self.adapter.create(text='A is the first letter of the alphabet.')
        statement_b = self.adapter.create(text='B is the second letter of the alphabet.')

        results = list(self.adapter.filter(order_by=['-text']))

        self.assertEqual(len(results), 2)
        self.assertEqual(results[1], statement_a)
        self.assertEqual(results[0], statement_b)


class StorageAdapterCreateTests(DjangoAdapterTestCase):
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
            StatementObject(text='A'),
            StatementObject(text='B')
        ])

        results = list(self.adapter.filter())

        self.assertEqual(len(results), 2)
        self.assertEqual(results[0].text, 'A')
        self.assertEqual(results[1].text, 'B')

    def test_create_many_search_text(self):
        self.adapter.create_many([
            StatementObject(text='A', search_text='a'),
            StatementObject(text='B', search_text='b')
        ])

        results = list(self.adapter.filter())

        self.assertEqual(len(results), 2)
        self.assertEqual(results[0].search_text, 'a')
        self.assertEqual(results[1].search_text, 'b')

    def test_create_many_search_in_response_to(self):
        self.adapter.create_many([
            StatementObject(text='A', search_in_response_to='a'),
            StatementObject(text='B', search_in_response_to='b')
        ])

        results = list(self.adapter.filter())

        self.assertEqual(len(results), 2)
        self.assertEqual(results[0].search_in_response_to, 'a')
        self.assertEqual(results[1].search_in_response_to, 'b')

    def test_create_many_tags(self):
        self.adapter.create_many([
            StatementObject(text='A', tags=['first', 'letter']),
            StatementObject(text='B', tags=['second', 'letter'])
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
            StatementObject(text='testing', tags=['ab', 'ab'])
        ])

        results = list(self.adapter.filter())

        self.assertEqual(len(results), 1)
        self.assertEqual(len(results[0].get_tags()), 1)
        self.assertEqual(results[0].get_tags(), ['ab'])


class StorageAdapterUpdateTests(DjangoAdapterTestCase):
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
