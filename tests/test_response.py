from .base_case import ChatBotTestCase


class ChatBotTests(ChatBotTestCase):

    def test_logging_timestamps(self):
        """
        Tests that the chat bot returns the correct datetime for logging
        """
        import datetime

        fmt = "%Y-%m-%d-%H-%M-%S"
        time = self.chatbot.timestamp(fmt)

        self.assertEqual(time, datetime.datetime.now().strftime(fmt))

    def test_chatbot_returns_answer_to_known_input(self):
        """
        Test that a matching response is returned when an exact
        match exists in the log files.
        """
        input_text = "What... is your favourite colour?"
        response = self.chatbot.get_response(input_text)

        output = ""
        for statement in response:
            output += statement["text"]

        self.assertTrue("Blue" in output)

    def test_match_is_last_line_in_file(self):
        """
        Make sure that the if the last line in a file matches the input text
        then a index error does not occure.
        """
        input_text = "Siri is my cat"
        response = self.chatbot.get_response(input_text)

        self.assertTrue(len(response) > 0)


    def test_input_text_returned_in_response_data(self):
        """
        This checks to see if a value is returned for the
        user name, timestamp and input text
        """
        user_name = "Ron Obvious"
        user_input = "Hello!"

        data = self.chatbot.get_response_data(user_name, user_input)

        self.assertEqual(data["user"]["name"], user_name)
        self.assertTrue(len(data["user"]["date"]) > 0)
        self.assertEqual(data["user"]["text"], user_input)

    def test_output_text_returned_in_response_data(self):
        """
        This checks to see if a value is returned for the
        bot name, timestamp and input text
        """
        user_name = "Sherlock"
        user_input = "Elementary my dear watson."

        data = self.chatbot.get_response_data(user_name, user_input)

        self.assertEqual(data["bot"][0]["name"], "Test Bot")
        self.assertTrue(len(data["bot"][0]["date"]) > 0)
        self.assertTrue(len(data["bot"][0]["text"]) > 0)

    def test_log_file_is_created(self):
        """
        Test that a log file is created when logging is set to true.
        """
        import os

        file_count_before = len([name for name in os.listdir(self.chatbot.log_directory)])

        # Submit input which should cause a new log to be created
        input_text = "What is the airspeed velocity of an unladen swallow?"
        response = self.chatbot.get_response(input_text)

        file_count_after = len([name for name in os.listdir(self.chatbot.log_directory)])

        self.assertTrue(file_count_before < file_count_after)

    def test_log_file_is_not_created_when_logging_is_set_to_false(self):
        """
        Test that a log file is not created when logging is set to false.
        """
        import os

        file_count_before = len([name for name in os.listdir(self.chatbot.log_directory)])

        # Force the chatbot to update it's timestamp
        self.chatbot.logging = False

        # Submit input which should cause a new log to be created
        input_text = "What is the airspeed velocity of an unladen swallow?"
        response = self.chatbot.get_response(input_text)

        file_count_after = len([name for name in os.listdir(self.chatbot.log_directory)])

        self.assertEqual(file_count_before, file_count_after)
