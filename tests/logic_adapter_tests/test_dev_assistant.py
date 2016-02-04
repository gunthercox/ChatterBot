from unittest import TestCase
from chatterbot.adapters.logic import DeveloperAssistant
from chatterbot.conversation import Statement


class DeveloperAssistantTests(TestCase):

    def setUp(self):
        self.adapter = DeveloperAssistant()

    def test_positive_input_single_statement(self):
        statement = Statement("run /main/tester.py")
        confidence, response = self.adapter.process(statement)

        self.assertEqual(confidence, 1)

    def test_positive_input_multi_statement(self):
        statement = Statement("run tester.py")
        confidence, response = self.adapter.process(statement)

        self.assertEqual(confidence, 1)
        self.assertIn("What is the absolute path to tester.py?", response.text)

    def test_negative_input(self):
        statement = Statement("What is an example of a pachyderm?")
        confidence, response = self.adapter.process(statement)

        self.assertEqual(confidence, 0)
