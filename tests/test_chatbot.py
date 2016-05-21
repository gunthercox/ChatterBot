from .base_case import ChatBotTestCase
from chatterbot.conversation import Statement, Response


class ChatterBotTests(ChatBotTestCase):

    def test_get_last_conversance(self):
        self.chatbot.recent_statements.append(
            (Statement("Test statement 1"), Statement("Test response 1"), )
        )
        self.chatbot.recent_statements.append(
            (Statement("Test statement 2"), Statement("Test response 2"), )
        )

        last_conversance = self.chatbot.get_last_conversance()
        self.assertEqual(last_conversance[0].text, "Test statement 2")
        self.assertEqual(last_conversance[1].text, "Test response 2")

    def test_no_last_conversance(self):
        self.assertIsNone(self.chatbot.get_last_conversance())

    def test_get_last_response_statement(self):
        """
        Make sure that the get last statement method
        returns the last statement that was issued.
        """
        self.chatbot.recent_statements.append(
            (Statement("Test statement 1"), Statement("Test response 1"), )
        )
        self.chatbot.recent_statements.append(
            (Statement("Test statement 2"), Statement("Test response 2"), )
        )

        last_statement = self.chatbot.get_last_response_statement()
        self.assertEqual(last_statement.text, "Test response 2")

    def test_no_last_response_statement(self):
        self.assertIsNone(self.chatbot.get_last_response_statement())

    def test_get_last_input_statement(self):
        """
        Make sure that the get last statement method
        returns the last statement that was issued.
        """
        self.chatbot.recent_statements.append(
            (Statement("Test statement 1"), Statement("Test response 1"), )
        )
        self.chatbot.recent_statements.append(
            (Statement("Test statement 2"), Statement("Test response 2"), )
        )

        last_statement = self.chatbot.get_last_input_statement()
        self.assertEqual(last_statement.text, "Test statement 2")

    def test_no_last_input_statement(self):
        self.assertIsNone(self.chatbot.get_last_input_statement())


class ChatterBotResponseTests(ChatBotTestCase):

    def setUp(self):
        super(ChatterBotResponseTests, self).setUp()

        response_list = [
            Response("Hi")
        ]

        self.test_statement = Statement("Hello", in_response_to=response_list)

    def test_empty_database(self):
        """
        If there is no statements in the database, then the
        user's input is the only thing that can be returned.
        """
        response = self.chatbot.get_response("How are you?")

        self.assertEqual("How are you?", response)

    def test_statement_saved_empty_database(self):
        """
        Test that when database is empty, the first
        statement is saved and returned as a response.
        """
        statement_text = "Wow!"
        response = self.chatbot.get_response(statement_text)

        saved_statement = self.chatbot.storage.find(statement_text)

        self.assertIsNotNone(saved_statement)
        self.assertEqual(response, statement_text)

    def test_statement_added_to_recent_response_list(self):
        """
        An input statement should be added to the recent response list.
        """
        statement_text = "Wow!"
        response = self.chatbot.get_response(statement_text)

        self.assertIn(statement_text, self.chatbot.recent_statements[0])
        self.assertEqual(response, statement_text)

    def test_response_known(self):
        self.chatbot.storage.update(self.test_statement)

        response = self.chatbot.get_response("Hi")

        self.assertEqual(response, self.test_statement.text)

    def test_response_format(self):
        self.chatbot.storage.update(self.test_statement)

        response = self.chatbot.get_response("Hi")
        statement_object = self.chatbot.storage.find(response)

        self.assertEqual(response, self.test_statement.text)
        self.assertEqual(len(statement_object.in_response_to), 1)
        self.assertIn("Hi", statement_object.in_response_to)

    def test_second_response_format(self):
        self.chatbot.storage.update(self.test_statement)

        response = self.chatbot.get_response("Hi")
        # response = "Hello"
        second_response = self.chatbot.get_response("How are you?")
        statement = self.chatbot.storage.find(second_response)

        # Make sure that the second response was saved to the database
        self.assertIsNotNone(self.chatbot.storage.find("How are you?"))

        self.assertEqual(second_response, self.test_statement.text)
        self.assertEqual(len(statement.in_response_to), 1)
        self.assertIn("Hi", statement.in_response_to)
