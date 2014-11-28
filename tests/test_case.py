from unittest import TestCase
from chatterbot import ChatBot


class ChatBotTestCase(TestCase):

    def setUp(self):
        """
        Create a set of log files for testing.
        """
        import os

        self.chatbot = ChatBot("Test Bot")

        if not os.path.exists(self.chatbot.log_directory):
            os.makedirs(self.chatbot.log_directory)

        log1 = open(self.chatbot.log_directory + "/log1", "w+")
        log1.write("robot,2014-10-15-15-18-22,How do know so much about swallows?\n")
        log1.write("user,2014-10-15-15-18-41,african or european?\n")
        log1.write("robot,2014-10-15-15-18-41,Huh? I... I don't know that.\n")
        log1.close()

        log2 = open(self.chatbot.log_directory + "/log2", "w+")
        log2.write("user,2014-10-15-15-17-31,Siri is adorable\n")
        log2.write("robot,2014-10-15-15-17-31,Who is Seri?\n")
        log2.write("user,2014-10-15-15-18-01,Siri is my cat\n")
        log2.close()

        log3 = open(self.chatbot.log_directory + "/log3", "w+")
        log3.write("Bridgekeeper,2014-10-15-15-17-31,What... is your quest?\n")
        log3.write("Sir Lancelot,2014-10-15-15-17-32,To seek the Holy Grail.\n")
        log3.write("Bridgekeeper,2014-10-15-15-17-33,What... is your favourite colour?\n")
        log3.write("Sir Lancelot,2014-10-15-15-17-34,Blue.\n")
        log3.close()

    def tearDown(self):
        """
        Remove the log files that were created for testing.
        """
        import os

        filelist = [ f for f in os.listdir(self.chatbot.log_directory)]
        for f in filelist:
            os.remove(self.chatbot.log_directory + "/" + f)

        os.rmdir(self.chatbot.log_directory)
