from .base_case import ChatBotTestCase


class ChatterBotStorageIntegrationTests(ChatBotTestCase):

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
