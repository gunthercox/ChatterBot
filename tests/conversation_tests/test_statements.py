# -*- coding: utf-8 -*-
from unittest import TestCase
from chatterbot.conversation import Statement


class StatementTests(TestCase):

    def setUp(self):
        self.statement = Statement("A test statement.")

    def test_string_equality(self):
        """
        It should be possible to check if a statement
        is the same as the statement text that another
        statement lists as a response.
        """
        self.assertEqual(self.statement, "A test statement.")

    def test_string_equality_unicode(self):
        """
        Test that it is possible to check if a statement
        is in a list of other statements when the
        statements text is unicode.
        """
        self.statement.text = "我很好太感谢"
        self.assertEqual(self.statement, "我很好太感谢")

    def test_serializer(self):
        data = self.statement.serialize()
        self.assertEqual(self.statement.text, data["text"])
