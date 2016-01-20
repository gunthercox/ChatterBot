from unittest import TestCase
from chatterbot.conversation.utils import get_response_statements
from chatterbot.conversation import Statement, Response


class ConversationUtilsTests(TestCase):

    def test_get_statements_with_known_responses(self):
        statement_list = [
            Statement("What... is your quest?"),
            Statement("This is a phone."),
            Statement("A what?", in_response_to=[Response("This is a phone.")]),
            Statement("A phone.", in_response_to=[Response("A what?")])
        ]

        responses = get_response_statements(statement_list)

        self.assertEqual(len(responses), 2)
        self.assertIn("This is a phone.", responses)
        self.assertIn("A what?", responses)
