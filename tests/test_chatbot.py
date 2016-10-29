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
        statement_object = self.chatbot.storage.find(response.text)

        self.assertEqual(response, self.test_statement.text)
        self.assertEqual(len(statement_object.in_response_to), 1)
        self.assertIn("Hi", statement_object.in_response_to)

    def test_second_response_format(self):
        self.chatbot.storage.update(self.test_statement)

        response = self.chatbot.get_response("Hi")
        # response = "Hello"
        second_response = self.chatbot.get_response("How are you?")
        statement = self.chatbot.storage.find(second_response.text)

        # Make sure that the second response was saved to the database
        self.assertIsNotNone(self.chatbot.storage.find("How are you?"))

        self.assertEqual(second_response, self.test_statement.text)
        self.assertEqual(len(statement.in_response_to), 1)
        self.assertIn("Hi", statement.in_response_to)

    def test_response_extra_data(self):
        """
        If an input statement has data contained in the
        `extra_data` attribute of a statement object,
        that data should saved with the input statement.
        """
        self.test_statement.add_extra_data("test", 1)
        self.chatbot.get_response(
            self.test_statement
        )

        saved_statement = self.chatbot.storage.find(
            self.test_statement.text
        )

        self.assertIn("test", saved_statement.extra_data)
        self.assertEqual(1, saved_statement.extra_data["test"])

    def test_generate_response(self):
        statement = Statement('Many insects adopt a tripedal gait for rapid yet stable walking.')
        input_statement, response, confidence = self.chatbot.generate_response(statement)

        self.assertEqual(input_statement, statement)
        self.assertEqual(response, statement)
        self.assertEqual(confidence, 1)

    def test_learn_response(self):
        statement = Statement('Hemoglobin is an oxygen-transport metalloprotein.')
        self.chatbot.learn_response(statement)
        exists = self.chatbot.storage.find(statement.text)

        self.assertIsNotNone(exists)

class ChatBotConfigFileTestCase(ChatBotTestCase):

    def setUp(self):
        super(ChatBotConfigFileTestCase, self).setUp()
        import json
        self.config_file_path = './test-config.json'
        self.data = self.get_kwargs()
        self.data['name'] = 'Config Test'

        with open(self.config_file_path, 'w+') as config_file:
            json.dump(self.data, config_file)

    def tearDown(self):
        super(ChatBotConfigFileTestCase, self).tearDown()
        import os

        if os.path.exists(self.config_file_path):
            os.remove(self.config_file_path)

    def test_read_from_config_file(self):
        from chatterbot import ChatBot
        self.chatbot = ChatBot.from_config(self.config_file_path)

        self.assertEqual(self.chatbot.name, self.data['name'])