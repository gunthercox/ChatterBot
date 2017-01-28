# -*- coding: utf-8 -*-
from unittest import TestCase
from chatterbot.conversation import Statement


class StatementTests(TestCase):

    def test_list_equality(self):
        """
        It should be possible to check if a statement
        exists in the list of statements that another
        statement has been issued in response to.
        """
        statements = [Statement('Hi'), Statement('Hello')]
        self.assertEqual(Statement('Hi'), statements)

    def test_list_equality_unicode(self):
        """
        Test that it is possible to check if a statement
        is in a list of other statements when the
        statements text is unicode.
        """
        statements = [Statement('Hello'), Statement('我很好太感谢')]
        self.assertIn(Statement('我很好太感谢'), statements)
