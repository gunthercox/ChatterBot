from django.test import TestCase
from chatterbot.storage import DjangoStorageAdapter
from chatterbot.ext.django_chatterbot.factories import (
    ConversationFactory,
    StatementFactory,
    ResponseFactory,
)
from chatterbot.ext.django_chatterbot.models import (
    Statement as StatementModel,
    Response as ResponseModel,
)


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

    def test_get_latest_response_from_invalid_conversation_id(self):
        response = self.adapter.get_latest_response(0)

        self.assertIsNone(response)

    def test_get_latest_response_from_zero_responses(self):
        conversation = ConversationFactory()
        response = self.adapter.get_latest_response(conversation.id)

        self.assertIsNone(response)

    def test_get_latest_response_from_one_responses(self):
        conversation = ConversationFactory()
        response_1 = ResponseFactory(
            statement=StatementFactory(text='A'),
            response=StatementFactory(text='B')
        )

        conversation.responses.add(response_1)
        response = self.adapter.get_latest_response(conversation.id)

        self.assertEqual(response_1.response, response)

    def test_get_latest_response_from_two_responses(self):
        conversation = ConversationFactory()
        response_1 = ResponseFactory(
            statement=StatementFactory(text='A'),
            response=StatementFactory(text='B')
        )
        response_2 = ResponseFactory(
            statement=StatementFactory(text='C'),
            response=StatementFactory(text='D')
        )

        conversation.responses.add(response_1, response_2)
        response = self.adapter.get_latest_response(conversation.id)

        self.assertEqual(response_2.response, response)

    def test_get_latest_response_from_three_responses(self):
        conversation = ConversationFactory()
        response_1 = ResponseFactory(
            statement=StatementFactory(text='A'),
            response=StatementFactory(text='B')
        )
        response_2 = ResponseFactory(
            statement=StatementFactory(text='C'),
            response=StatementFactory(text='D')
        )
        response_3 = ResponseFactory(
            statement=StatementFactory(text='E'),
            response=StatementFactory(text='F')
        )

        conversation.responses.add(response_1, response_2, response_3)
        response = self.adapter.get_latest_response(conversation.id)

        self.assertEqual(response_3.response, response)

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

        self.assertTrue(result.responses.filter(statement__text="Yes").exists())
        self.assertTrue(result.responses.filter(statement__text="No").exists())

    def test_multiple_responses_added_on_update(self):
        statement = StatementModel.objects.create(text="You are welcome.")
        statement.add_response(StatementModel(text="Thank you."))
        statement.add_response(StatementModel(text="Thanks."))

        self.adapter.update(statement)

        result = self.adapter.find(statement.text)

        self.assertEqual(result.responses.count(), 2)
        self.assertTrue(result.responses.filter(statement__text="Thank you.").exists())
        self.assertTrue(result.responses.filter(statement__text="Thanks.").exists())

    def test_update_saves_statement_with_multiple_responses(self):
        statement = StatementModel.objects.create(text="You are welcome.")
        statement.add_response(StatementModel(text="Thanks."))
        statement.add_response(StatementModel(text="Thank you."))

        self.adapter.update(statement)

        response = self.adapter.find(statement.text)

        self.assertEqual(ResponseModel.objects.count(), 2)
        self.assertEqual(response.responses.count(), 2)

    def test_getting_and_updating_statement(self):
        statement = StatementModel.objects.create(text="Hi")
        statement.add_response(StatementModel(text="Hello"))
        statement.add_response(StatementModel(text="Hello"))

        self.adapter.update(statement)

        response = self.adapter.find(statement.text)

        self.assertEqual(response.responses.count(), 2)
        self.assertEqual(response.responses.first().occurrence, 2)

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
        self.assertTrue(responses.filter(in_response__statement__text="This is a phone.").exists())
        self.assertTrue(responses.filter(in_response__statement__text="A what?").exists())


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

        results = self.adapter.filter(in_response_to="Maybe")
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
        response = response.first()

        self.assertEqual(response.responses.count(), 2)

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

        self.assertEqual(found.count(), 1)
        self.assertEqual(found.first().responses.count(), 1)
        self.assertEqual(type(found.first().responses.first()), ResponseModel)

    def test_confidence(self):
        """
        Test that the confidence value is not saved to the database.
        The confidence attribute on statements is intended to just hold
        the confidence of the statement when it returned as a response to
        some input. Because of that, the value of the confidence score
        should never be stored in the database with the statement.
        """
        statement = StatementModel(text='Test statement')
        statement.confidence = 0.5
        statement.save()

        statement_updated = StatementModel.objects.get(pk=statement.id)

        self.assertEqual(statement_updated.confidence, 0)


class DjangoOrderingTestCase(DjangoStorageAdapterTestCase):
    """
    Test cases for the ordering of sets of statements.
    """

    def test_order_by_text(self):
        statement_a = StatementModel.objects.create(text='A is the first letter of the alphabet.')
        statement_b = StatementModel.objects.create(text='B is the second letter of the alphabet.')

        results = self.adapter.filter(order_by='text')

        self.assertEqual(len(results), 2)
        self.assertEqual(results[0], statement_a)
        self.assertEqual(results[1], statement_b)

    def test_reverse_order_by_text(self):
        statement_a = StatementModel.objects.create(text='A is the first letter of the alphabet.')
        statement_b = StatementModel.objects.create(text='B is the second letter of the alphabet.')

        results = self.adapter.filter(order_by='-text')

        self.assertEqual(len(results), 2)
        self.assertEqual(results[1], statement_a)
        self.assertEqual(results[0], statement_b)
