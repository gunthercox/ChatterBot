from unittest import TestCase
from chatterbot.conversation import Statement


class StatementTests(TestCase):

    def setUp(self):
        self.statement = Statement("A test statement.")

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
        # TODO
        self.assertTrue(True)

    def test_serializer(self):
        # TODO
        self.assertTrue(True)


class SignatureTests(TestCase):

    def setUp(self):
        self.signature = Signature("Gunther Cox")

    def test_add_timestamp(self):
        """
        Tests that the correct timestamp is returned.
        """
        import datetime

        fmt = "%Y-%m-%d-%H-%M-%S"
        time = self.signature.create_timestamp(fmt)

        now = datetime.datetime.now().strftime(fmt)

        self.assertEqual(time, now)
