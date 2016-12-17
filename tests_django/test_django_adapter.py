import os
from django.test import TestCase
from chatterbot.storage import DjangoStorageAdapter
from chatterbot.ext.django_chatterbot.models import Statement as StatementModel
from chatterbot.ext.django_chatterbot.models import Response as ResponseModel


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


class DjangoStorageAdapterTestCase(DjangoAdapterTestCase):

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
        statement = StatementModel(text="Test statement")
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
        statement = StatementModel.objects.create(text="New statement")

        found_statement = self.adapter.find("New statement")
        self.assertNotEqual(found_statement, None)
        self.assertEqual(found_statement.text, statement.text)

    def test_update_adds_new_statement(self):
        statement = StatementModel.objects.create(text="New statement")

        statement_found = self.adapter.find("New statement")
        self.assertNotEqual(statement_found, None)
        self.assertEqual(statement_found.text, statement.text)

    def test_update_modifies_existing_statement(self):
        statement = StatementModel.objects.create(text="New statement")
        other_statement = StatementModel.objects.create(text="New response")

        # Check the initial values
        found_statement = self.adapter.find(statement.text)
        self.assertEqual(len(found_statement.in_response_to), 0)

        statement.in_response.create(
            statement=statement,
            response=other_statement
        )
        # Update the statement value
        self.adapter.update(statement)

        # Check that the values have changed
        found_statement = self.adapter.find(statement.text)
        self.assertEqual(len(found_statement.in_response_to), 1)

    def test_get_random_returns_statement(self):
        statement = StatementModel.objects.create(text="New statement")

        random_statement = self.adapter.get_random()
        self.assertEqual(random_statement.text, statement.text)

    def test_find_returns_nested_responses(self):
        statement = StatementModel.objects.create(text="Do you like this?")
        statement.add_response(StatementModel(text="Yes"))
        statement.add_response(StatementModel(text="No"))

        self.adapter.update(statement)

        result = self.adapter.find(statement.text)

        self.assertTrue(result.in_response_to.filter(response__text="Yes").exists())
        self.assertTrue(result.in_response_to.filter(response__text="No").exists())

    def test_multiple_responses_added_on_update(self):
        statement = StatementModel.objects.create(text="You are welcome.")
        statement.add_response(StatementModel(text="Thank you."))
        statement.add_response(StatementModel(text="Thanks."))

        self.adapter.update(statement)

        result = self.adapter.find(statement.text)

        self.assertEqual(result.in_response_to.count(), 2)
        self.assertTrue(result.in_response_to.filter(response__text="Thank you.").exists())
        self.assertTrue(result.in_response_to.filter(response__text="Thanks.").exists())

    def test_update_saves_statement_with_multiple_responses(self):
        statement = StatementModel.objects.create(text="You are welcome.")
        statement.add_response(StatementModel(text="Thanks."))
        statement.add_response(StatementModel(text="Thank you."))

        self.adapter.update(statement)

        response = self.adapter.find(statement.text)

        self.assertEqual(response.in_response_to.count(), 2)

    def test_getting_and_updating_statement(self):
        statement = StatementModel.objects.create(text="Hi")
        statement.add_response(StatementModel(text="Hello"))
        statement.add_response(StatementModel(text="Hello"))

        self.adapter.update(statement)

        response = self.adapter.find(statement.text)

        self.assertEqual(len(response.in_response_to), 1)
        self.assertEqual(response.in_response_to[0].occurrence, 2)

    def test_remove(self):
        text = "Sometimes you have to run before you can walk."
        statement = StatementModel.objects.create(text=text)

        self.adapter.remove(statement.text)
        result = self.adapter.find(text)

        self.assertIsNone(result)

    def test_remove_response(self):
        text = "Sometimes you have to run before you can walk."
        statement = StatementModel.objects.create(
            text="A test flight is not recommended at this design phase."
        )
        statement.add_response(
            StatementModel(text=text)
        )
        self.adapter.remove(statement.text)
        results = self.adapter.filter(in_response_to__contains=text)

        self.assertEqual(results.count(), 0)

    def test_get_response_statements(self):
        """
        Test that we are able to get a list of only statements
        that are known to be in response to another statement.
        """
        s1 = StatementModel(text="What... is your quest?")
        s2 = StatementModel(text="This is a phone.")
        s3 = StatementModel(text="A what?")
        s4 = StatementModel(text="A phone.")

        s3.add_response(s2)
        s4.add_response(s3)

        for statement in [s1, s2, s3, s4]:
            self.adapter.update(statement)

        responses = self.adapter.get_response_statements()

        self.assertEqual(len(responses), 2)
        self.assertTrue(responses.filter(in_response__response__text="This is a phone.").exists())
        self.assertTrue(responses.filter(in_response__response__text="A what?").exists())


class DjangoAdapterFilterTestCase(DjangoAdapterTestCase):

    def setUp(self):
        super(DjangoAdapterFilterTestCase, self).setUp()

        self.statement1 = StatementModel(text="Testing...")
        self.statement1.add_response(
            StatementModel(text="Why are you counting?")
        )

        self.statement2 = StatementModel(text="Testing one, two, three.")
        self.statement2.add_response(self.statement1)

    def test_filter_text_no_matches(self):
        self.adapter.update(self.statement1)
        results = self.adapter.filter(text="Howdy")

        self.assertEqual(len(results), 0)

    def test_filter_in_response_to_no_matches(self):
        self.adapter.update(self.statement1)

        results = self.adapter.filter(
            in_response_to__response__text="Maybe"
        )
        self.assertEqual(len(results), 0)

    def test_filter_equal_results(self):
        statement1 = StatementModel(text="Testing...")
        statement2 = StatementModel(text="Testing one, two, three.")

        self.adapter.update(statement1)
        self.adapter.update(statement2)

        results = self.adapter.filter(in_response_to=[])

        self.assertEqual(results.count(), 2)
        self.assertTrue(results.filter(text=statement1.text).exists())
        self.assertTrue(results.filter(text=statement2.text).exists())

    def test_filter_contains_result(self):
        self.adapter.update(self.statement1)
        self.adapter.update(self.statement2)

        results = self.adapter.filter(
            in_response_to__contains="Why are you counting?"
        )
        self.assertEqual(results.count(), 1)
        self.assertTrue(results.filter(text=self.statement1.text).exists())

    def test_filter_contains_no_result(self):
        self.adapter.update(self.statement1)

        results = self.adapter.filter(
            in_response_to__contains="How do you do?"
        )
        self.assertEqual(results.count(), 0)

    def test_filter_multiple_parameters(self):
        self.adapter.update(self.statement1)
        self.adapter.update(self.statement2)

        results = self.adapter.filter(
            text="Testing...",
            in_response_to__contains="Why are you counting?"
        )

        self.assertEqual(results.count(), 1)
        self.assertTrue(results.filter(text=self.statement1.text).exists())

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
        statement1 = StatementModel(text="Testing...")
        statement2 = StatementModel(text="Testing one, two, three.")
        self.adapter.update(statement1)
        self.adapter.update(statement2)

        results = self.adapter.filter()

        self.assertEqual(len(results), 2)

    def test_filter_returns_statement_with_multiple_responses(self):
        statement = StatementModel.objects.create(text="You are welcome.")
        statement.add_response(StatementModel(text="Thanks."))
        statement.add_response(StatementModel(text="Thank you."))

        self.adapter.update(statement)

        response = self.adapter.filter(
            in_response_to__contains="Thanks."
        )

        # Get the first response
        response = response[0]

        self.assertEqual(len(response.in_response_to), 2)

    def test_response_list_in_results(self):
        """
        If a statement with response values is found using the filter
        method, they should be returned as response objects.
        """
        statement = StatementModel.objects.create(
            text="The first is to help yourself, the second is to help others.",
        )
        statement.add_response(StatementModel(text="Why do people have two hands?"))

        self.adapter.update(statement)

        found = self.adapter.filter(text=statement.text)

        self.assertEqual(len(found[0].in_response_to), 1)
        self.assertEqual(type(found[0].in_response_to[0]), ResponseModel)


class ReadOnlyDjangoAdapterTestCase(DjangoAdapterTestCase):

    def test_update_does_not_add_new_statement(self):
        self.adapter.read_only = True

        statement = StatementModel(text="New statement")
        self.adapter.update(statement)

        statement_found = self.adapter.find("New statement")
        self.assertEqual(statement_found, None)

    def test_update_does_not_modify_existing_statement(self):
        statement = StatementModel.objects.create(text="New statement")

        self.adapter.read_only = True

        statement.add_response(
            StatementModel(text="New response")
        )
        self.adapter.update(statement)

        statement_found = self.adapter.find("New statement")
        self.assertEqual(statement_found.text, statement.text)
        self.assertEqual(len(statement_found.in_response_to), 0)
