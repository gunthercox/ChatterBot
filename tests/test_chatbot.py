from .base_case import ChatBotTestCase


class ChatBotTests(ChatBotTestCase):

    def test_get_last_statement(self):
        """
        Make sure that the get last statement method
        returns the last statement that was issued.
        """
        self.chatbot.last_statements.append("Test statement")

        self.assertEqual(self.chatbot.get_last_statement(), "Test statement")

    def test_logging_timestamps(self):
        """
        Tests that the chat bot returns the correct
        datetime for logging
        """
        import datetime

        fmt = "%Y-%m-%d-%H-%M-%S"
        time = self.chatbot.timestamp(fmt)

        self.assertEqual(time, datetime.datetime.now().strftime(fmt))

    def test_training_adds_statements(self):
        """
        Ensure that the training method adds statements
        to the database.
        """

        conversation = [
            "Hello",
            "Hi there!",
            "How are you doing?",
            "I'm great.",
            "That is good to hear",
            "Thank you.",
            "You are welcome.",
            "Sure, any time.",
            "Yeah",
            "Can I help you with anything?"
        ]

        self.chatbot.train(conversation)

        self.assertEqual(self.chatbot.get_response("Thank you."), "You are welcome.")

    def test_training_increments_occurrence_count(self):
        
        conversation = [
            "Do you like my hat?",
            "I do not like your hat."
        ]

        self.chatbot.train(conversation)
        self.chatbot.train(conversation)

        count = self.chatbot.database["Do you like my hat?"]["occurrence"]
        self.assertEqual(count, 2)

    def test_chatbot_returns_answer_to_known_input(self):
        """
        Test that a matching response is returned when an
        exact match exists in the log files.
        """
        input_text = "What... is your favourite colour?"
        response = self.chatbot.get_response(input_text)

        self.assertIn("Blue", response)

    def test_chatbot_returns_answer_close_to_known_input(self):
 
        input_text = "What is your favourite colour?"
        response = self.chatbot.get_response(input_text)

        self.assertIn("Blue", response)

    def test_match_is_last_line_in_file(self):
        """
        Make sure that the if the last line in a file
        matches the input text then a index error does
        not occure.
        """
        input_text = "Siri is my cat"
        response = self.chatbot.get_response(input_text)

        self.assertGreater(len(response), 0)


    def test_input_text_returned_in_response_data(self):
        """
        This checks to see if a value is returned for the
        user name, timestamp and input text
        """
        user_name = "Ron Obvious"
        user_input = "Hello!"

        data = self.chatbot.get_response_data(user_name, user_input)

        self.assertIn(user_input, data[user_name].keys())

    def test_output_text_returned_in_response_data(self):
        """
        This checks to see if a value is returned for the
        bot name, timestamp and input text
        """
        user_name = "Sherlock"
        user_input = "Elementary my dear watson."

        data = self.chatbot.get_response_data(user_name, user_input)

        self.assertGreater(len(data["bot"]), 0)

    def test_log_file_is_updated(self):
        """
        Test that a log file is updated when logging is
        set to true.
        """
        import os

        file_size_before = os.path.getsize(self.chatbot.database.path)

        # Force the chatbot to update it's timestamp
        self.chatbot.log = True

        # Submit input which should cause a new log to be created
        input_text = "What is the airspeed velocity of an unladen swallow?"
        response = self.chatbot.get_response(input_text)

        file_size_after = os.path.getsize(self.chatbot.database.path)

        self.assertLess(file_size_before, file_size_after)

    def test_log_file_is_not_updated_when_logging_is_set_to_false(self):
        """
        Test that a log file is not created when logging
        is set to false.
        """
        import os

        file_size_before = os.path.getsize(self.chatbot.database.path)

        # Force the chatbot to update it's timestamp
        self.chatbot.log = False

        # Submit input which should cause a new log to be created
        input_text = "What is the airspeed velocity of an unladen swallow?"
        response = self.chatbot.get_response(input_text)

        file_size_after = os.path.getsize(self.chatbot.database.path)

        self.assertEqual(file_size_before, file_size_after)
