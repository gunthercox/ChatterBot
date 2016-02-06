from unittest import TestCase
from chatterbot.conversation import Statement, Response


class StatementTests(TestCase):

    def setUp(self):
        self.statement = Statement("A test statement.")

    def test_equality(self):
        """
        It should be possible to check if a statement
        exists in the list of statements that another
        statement has been issued in response to.
        """
        self.statement.add_response(Response("Yo"))
        self.assertEqual(len(self.statement.in_response_to), 1)
        self.assertIn(Response("Yo"), self.statement.in_response_to)

    def test_update_response_list_new(self):
        self.statement.add_response(Response("Hello"))
        self.assertTrue(len(self.statement.in_response_to), 1)

    def test_update_response_list_existing(self):
        response = Response("Hello")
        self.statement.add_response(response)
        self.statement.add_response(response)
        self.assertTrue(len(self.statement.in_response_to), 1)

    def test_remove_response_exists(self):
        self.statement.add_response(Response("Testing"))
        removed = self.statement.remove_response("Testing")
        self.assertTrue(removed)

    def test_remove_response_does_not_exist(self):
        self.statement.add_response(Response("Testing"))
        removed = self.statement.remove_response("Test")
        self.assertFalse(removed)

    def test_serializer(self):
        data = self.statement.serialize()
        self.assertEqual(self.statement.text, data["text"])

    def test_occurrence_count_for_new_statement(self):
        """
        When the occurrence is updated for a statement that
        previously did not exist as a statement that the current
        statement was issued in response to, then the new statement
        should be added to the response list and the occurence count
        for that response should be set to 1.
        """
        response = Response("This is a test.")

        self.statement.add_response(response)
        self.assertTrue(self.statement.get_response_count(response), 1)

    def test_occurrence_count_for_existing_statement(self):
        self.statement.add_response(Response("ABC"))
        self.statement.add_response(Response("ABC"))
        self.assertTrue(
            self.statement.get_response_count(Response("ABC")),
            2
        )

    def test_occurrence_count_incremented(self):
        self.statement.add_response(Response("ABC"))
        self.statement.add_response(Response("ABC"))

        self.assertEqual(len(self.statement.in_response_to), 1)
        self.assertEqual(self.statement.in_response_to[0].occurrence, 2)
