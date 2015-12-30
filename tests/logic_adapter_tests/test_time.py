from unittest import TestCase
from chatterbot.adapters.logic import TimeLogicAdapter
from chatterbot.conversation import Statement


class TimeAdapterTests(TestCase):

    def setUp(self):
        self.adapter = TimeLogicAdapter()

    def test_positive_input(self):
        statement = Statement("Do you know what time it is?")
        confidence, response = self.adapter.process(statement)

        self.assertEqual(confidence, 1)
        self.assertIn("The current time is ", response.text)

    def test_negative_input(self):
        statement = Statement("What is an example of a pachyderm?")
        confidence, response = self.adapter.process(statement)

        self.assertEqual(confidence, 0)
        self.assertIn("The current time is ", response.text)

