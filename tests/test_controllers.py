from .base_case import ChatBotTestCase
from chatterbot.controllers import StorageController


class ControllerTests(ChatBotTestCase):

    def test_get_last_statement(self):
        """
        Make sure that the get last statement method
        returns the last statement that was issued.
        """
        self.controller.recent_statements.append("Test statement 1")
        self.controller.recent_statements.append("Test statement 2")
        self.controller.recent_statements.append("Test statement 3")

        self.assertEqual(self.controller.get_last_statement(), "Test statement 3")

    def test_get_most_frequent_response(self):

        output = self.controller.get_most_frequent_response("What... is your quest?")

        self.assertEqual("To seek the Holy Grail.", list(output.keys())[0])

