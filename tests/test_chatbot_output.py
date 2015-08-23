from .base_case import ChatBotTestCase, UntrainedChatBotTestCase
from chatterbot.conversation import Statement


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
        output = self.chatbot.get_most_frequent_response(
            Statement("What... is your quest?")
        )

        self.assertEqual("To seek the Holy Grail.", output)

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


class ResponseTestCase(UntrainedChatBotTestCase):

    def test_empty_database(self):
        """
        If there is no statements in the database, then the
        user's input is the only thing that can be returned.
        """
        response = self.chatbot.get_response("How are you?")

        self.assertEqual("How are you?", response)


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

