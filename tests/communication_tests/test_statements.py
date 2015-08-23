from unittest import TestCase
from chatterbot.conversation import Statement, Signature


class StatementTests(TestCase):

    def setUp(self):
        self.statement = Statement("A test statement.")

    def test_equality(self):
        """
        It should be possible to check if a statement
        exists in the list of statements that another
        statement has been issued in response to.
        """
        self.statement.add_response(Statement("Yo"))
        self.assertEqual(len(self.statement.in_response_to), 1)
        self.assertIn(
            Statement("Yo"),
            self.statement.in_response_to
        )

    def test_occurrence_count(self):
        self.statement.update_occurrence_count()
        self.assertTrue(
            self.statement.get_occurrence_count(),
            2
        )

    def test_update_response_list_new(self):
        new_statement = Statement("Hello")
        self.statement.add_response(new_statement)
        self.assertTrue(
            len(self.statement.in_response_to),
            1
        )

    def test_update_response_list_existing(self):
        previous_statement = Statement("Hello")
        self.statement.add_response(previous_statement)
        self.statement.add_response(previous_statement)
        self.assertTrue(
            len(self.statement.in_response_to),
            1
        )

    def test_add_signature(self):
        signature = Signature("Gunther Cox")
        self.statement.add_signature(signature)
        self.assertIn(signature, self.statement.signatures)

    def test_serializer(self):
        data = self.statement.serialize()
        self.assertEqual(self.statement.text, data["text"])

