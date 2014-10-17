from unittest import TestCase
from chatterbot import ChatBot


class Tests(TestCase):

    def setUp(self):
        """
        Create a set of log files for testing.
        """
        import os

        self.directory = "conversation_engrams/"

        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

        log1 = open(self.directory + "/log1", "w+")
        log1.write("robot,2014-10-15-15-18-22,How do know so much about swallows?\n")
        log1.write("user,2014-10-15-15-18-41,african or european?\n")
        log1.write("robot,2014-10-15-15-18-41,Huh? I... I don't know that.\n")
        log1.close()

        log2 = open(self.directory + "/log2", "w+")
        log2.write("user,2014-10-15-15-17-31,Siri is adorable\n")
        log2.write("robot,2014-10-15-15-17-31,Who is Seri?\n")
        log2.write("user,2014-10-15-15-18-01,Siri is my cat\n")
        log2.close()

        log3 = open(self.directory + "/log3", "w+")
        log3.write("Bridgekeeper,0,What... is your quest?\n")
        log3.write("Sir Lancelot,0,To seek the Holy Grail.\n")
        log3.write("Bridgekeeper,0,What... is your favourite colour?\n")
        log3.write("Sir Lancelot,0,Blue.\n")
        log3.close()

    def tearDown(self):
        """
        Remove the log files that were created for testing.
        """
        import os

        filelist = [ f for f in os.listdir(self.directory)]
        for f in filelist:
            os.remove(self.directory + "/" + f)

        os.rmdir(self.directory)

    def test_logging_timestamps(self):
        """
        Tests that the chat bot returns the correct datetime for logging
        """
        import datetime

        chatbot = ChatBot()
        fmt = "%Y-%m-%d-%H-%M-%S"
        t = chatbot.timestamp(fmt)

        self.assertEqual(t, datetime.datetime.now().strftime(fmt))

    def test_chatbot_returns_answer_to_known_input(self):
        """
        Test that a matching response is returned when an exact
        match exists in the log files.
        """
        input_text = "What... is your favourite colour?"
        chatbot = ChatBot()
        response = chatbot.get_response(input_text)

        self.assertTrue("Blue" in response)

    def test_match_is_last_line_in_file(self):
        """
        Make sure that the if the last line in a file matches the input text
        then a index error does not occure.
        """
        input_text = "Siri is my cat"
        chatbot = ChatBot()
        response = chatbot.get_response(input_text)

        self.assertTrue(len(response) > 0)


    def test_input_text_returned_in_response_data(self):
        """
        This checks to see if a value is returned for the
        user name, timestamp and input text
        """
        user_name = "Ron Obvious"
        user_input = "Hello!"

        chatbot = ChatBot()
        data = chatbot.get_response_data(user_name, user_input)

        self.assertEqual(data["user"]["name"], user_name)
        self.assertTrue(len(data["user"]["timestamp"]) > 0)
        self.assertEqual(data["user"]["text"], user_input)

    def test_output_text_returned_in_response_data(self):
        """
        This checks to see if a value is returned for the
        bot name, timestamp and input text
        """
        user_name = "Sherlock"
        user_input = "Elementary my dear watson."

        chatbot = ChatBot("Watson")
        data = chatbot.get_response_data(user_name, user_input)

        self.assertEqual(data["bot"]["name"], "Watson")
        self.assertTrue(len(data["bot"]["timestamp"]) > 0)
        self.assertTrue(len(data["bot"]["text"]) > 0)

    def test_twitter_api(self):
        """
        Make sure that results from the twitter api can be used.
        """
        pass
