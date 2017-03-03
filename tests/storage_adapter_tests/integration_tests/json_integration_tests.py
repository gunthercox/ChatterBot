from tests.base_case import ChatBotTestCase


class JsonStorageIntegrationTests(ChatBotTestCase):

    def test_database_is_updated(self):
        """
        Test that the database is updated when read_only is set to false.
        """
        input_text = 'What is the airspeed velocity of an unladen swallow?'
        exists_before = self.chatbot.storage.find(input_text)

        response = self.chatbot.get_response(input_text)
        exists_after = self.chatbot.storage.find(input_text)

        self.assertFalse(exists_before)
        self.assertTrue(exists_after)
