from .base_case import ChatBotTestCase
from chatterbot.controllers import StorageController


class ControllerTests(ChatBotTestCase):

    def setUp(self):
        """
        Set up a controller and database for testing.
        """
        super(ControllerTests, self).setUp()

        adapter = self.chatbot.storage_adapter
        self.controller = StorageController(adapter)

    def test_get_last_statement(self):
        """
        Make sure that the get last statement method
        returns the last statement that was issued.
        """
        self.controller.recent_statements.append("Test statement 1")
        self.controller.recent_statements.append("Test statement 2")
        self.controller.recent_statements.append("Test statement 3")

        self.assertEqual(self.controller.get_last_statement(), "Test statement 3")

    def test_update_occurrence_count(self):
        count = self.controller.update_occurrence_count({"occurrence": 3})

        self.assertTrue(count > 3)

    def test_update_response_list(self):
        previous_statement = "Greetings Dr. Jones."
        response_list = self.controller.update_response_list("Yo", previous_statement)

        self.assertTrue(previous_statement in response_list)

    def test_get_most_frequent_response(self):

        output = self.controller.get_most_frequent_response("What... is your quest?")

        self.assertEqual("To seek the Holy Grail.", list(output.keys())[0])


    def tearDown(self):
        """
        Remove the test database.
        """
        self.controller.storage_adapter.drop()
