from .base_case import ChatBotTestCase, UntrainedChatBotTestCase
from chatterbot.conversation import Statement, Response


class ChatBotOutputTests(ChatBotTestCase):

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
            Statement("What... is your quest?", occurrence=2),
            Statement("This is a phone.", occurrence=4),
            Statement("A what?", occurrence=2),
            Statement("A phone.", occurrence=2)
        ]

        # Save each statement to the database
        for statement in statement_list:
            self.chatbot.storage.update(statement)

        output = self.chatbot.get_most_frequent_response(
            statement_list
        )

        self.assertEqual("This is a phone.", output)

    def test_get_first_response(self):
        statement_list = [
            Statement("What... is your quest?", occurrence=2),
            Statement("A what?", occurrence=2),
            Statement("A quest.", occurrence=2)
        ]

        output = self.chatbot.get_first_response(
            statement_list
        )

        self.assertEqual("What... is your quest?", output)

    def test_get_random_response(self):
        statement_list = [
            Statement("This is a phone.", occurrence=4),
            Statement("A what?", occurrence=2),
            Statement("A phone.", occurrence=2)
        ]

        output = self.chatbot.get_random_response(
            statement_list
        )

        self.assertTrue(output)

    def test_answer_to_known_input(self):
        """
        Test that a matching response is returned
        when an exact match exists.
        """
        input_text = "What... is your favourite colour?"
        response = self.chatbot.get_response(input_text)

        self.assertIn("Blue", response)

    def test_answer_close_to_known_input(self):

        input_text = "What is your favourite colour?"
        response = self.chatbot.get_response(input_text)

        self.assertIn("Blue", response)

    def test_match_has_no_response(self):
        """
        Make sure that the if the last line in a file
        matches the input text then a index error does
        not occure.
        """
        input_text = "Siri is my cat"
        response = self.chatbot.get_response(input_text)

        self.assertGreater(len(response), 0)

    def test_empty_input(self):
        """
        If empty input is provided, anything may be returned.
        """
        output = self.chatbot.get_response("")

        self.assertTrue(len(output) > -1)


class ChatterBotResponseTestCase(UntrainedChatBotTestCase):

    def setUp(self):
        super(ChatterBotResponseTestCase, self).setUp()

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
        #TODO: self.assertEqual(statement_object.get_occurrence_count(), 2)
        self.assertEqual(len(statement_object.in_response_to), 1)
        self.assertIn("Hi", statement_object.in_response_to)

    def test_second_response_format(self):
        self.chatbot.storage.update(self.test_statement)

        response = self.chatbot.get_response("Hi")
        # response = "Hello"
        second_response = self.chatbot.get_response("How are you?")
        statement_object = self.chatbot.storage.find(second_response)

        self.assertEqual(second_response, self.test_statement.text)
        #TODO: self.assertEqual(statement_object.get_response_count(), 2)
        self.assertEqual(len(statement_object.in_response_to), 1)
        self.assertIn("Hi", statement_object.in_response_to)


class ChatterBotStorageIntegrationTests(UntrainedChatBotTestCase):

    def test_database_is_updated(self):
        """
        Test that the database is updated when read_only is set to false.
        """
        input_text = "What is the airspeed velocity of an unladen swallow?"
        exists_before = self.chatbot.storage.find(input_text)

        response = self.chatbot.get_response(input_text)
        exists_after = self.chatbot.storage.find(input_text)

        self.assertFalse(exists_before)
        self.assertTrue(exists_after)

    def test_database_is_not_updated_when_read_only(self):
        """
        Test that the database is not updated when read_only is set to true.
        """
        self.chatbot.storage.read_only = True

        input_text = "Who are you? The proud lord said."
        exists_before = self.chatbot.storage.find(input_text)

        response = self.chatbot.get_response(input_text)
        exists_after = self.chatbot.storage.find(input_text)

        self.assertFalse(exists_before)
        self.assertFalse(exists_after)
