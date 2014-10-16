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

    def test_chatbot_returns_answer_to_known_input(self):

        input_text = "What... is your favourite colour?"
        chatbot = ChatBot()
        response = chatbot.get_response(input_text)

        self.assertTrue("Blue" in response)

    def test_match_is_last_line_in_file(self):

        input_text = "Siri is my cat"
        chatbot = ChatBot()
        response = chatbot.get_response(input_text)

        self.assertTrue(len(response) > 0)

    def test_twitter_api(self):
        """
        Make sure that results from the twitter api can be used.
        """
        pass
