from .base_case import ChatBotTestCase
from chatterbot.conversation import Statement, Response


class ChatterBotTests(ChatBotTestCase):

    def test_get_last_statement(self):
        """
        Make sure that the get last statement method
        returns the last statement that was issued.
        """
        self.chatbot.recent_statements.append(
            Statement("Test statement 1")
        )
        self.chatbot.recent_statements.append(
            Statement("Test statement 2")
        )
        self.chatbot.recent_statements.append(
            Statement("Test statement 3")
        )

        last_statement = self.chatbot.get_last_statement()
        self.assertEqual(last_statement.text, "Test statement 3")

    def test_get_most_frequent_response(self):
        statement_list = [
            Statement("What... is your quest?", in_response_to=[Response("Hello", occurrence=2)]),
            Statement("This is a phone.", in_response_to=[Response("Hello", occurrence=4)]),
            Statement("A what?", in_response_to=[Response("Hello", occurrence=2)]),
            Statement("A phone.", in_response_to=[Response("Hello", occurrence=1)])
        ]

        # Save each statement to the database
        for statement in statement_list:
            self.chatbot.storage.update(statement)

        output = self.chatbot.get_most_frequent_response(
            Statement("Hello"),
            statement_list
        )

        self.assertEqual("This is a phone.", output)

    def test_get_first_response(self):
        statement_list = [
            Statement("What... is your quest?"),
            Statement("A what?"),
            Statement("A quest.")
        ]

        output = self.chatbot.get_first_response(
            statement_list
        )

        self.assertEqual("What... is your quest?", output)

    def test_get_random_response(self):
        statement_list = [
            Statement("This is a phone."),
            Statement("A what?"),
            Statement("A phone.")
        ]

        output = self.chatbot.get_random_response(
            statement_list
        )

        self.assertTrue(output)


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
        A new input statement should be added to the recent response list.
        """
        statement_text = "Wow!"
        response = self.chatbot.get_response(statement_text)

        self.assertIn(statement_text, self.chatbot.recent_statements)
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

        self.assertEqual(second_response, self.test_statement.text)
        self.assertEqual(len(statement.in_response_to), 1)
        self.assertIn("Hi", statement.in_response_to)

