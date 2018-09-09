from tests.base_case import ChatBotSQLTestCase


class SqlStorageIntegrationTests(ChatBotSQLTestCase):

    def test_database_is_updated(self):
        """
        Test that the database is updated when read_only is set to false.
        """
        input_text = 'What is the airspeed velocity of an unladen swallow?'
        exists_before = self.chatbot.storage.filter(text=input_text)

        self.chatbot.get_response(input_text)
        exists_after = self.chatbot.storage.filter(text=input_text)

        self.assertEqual(len(exists_before), 0)
        self.assertTrue(len(exists_after), 1)
