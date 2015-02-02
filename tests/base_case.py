from unittest import TestCase
from chatterbot import ChatBot


class ChatBotTestCase(TestCase):

    def setUp(self):
        """
        Create a set of log files for testing.
        """
        import os, json

        data = {
            "Huh? I... I don't know that.": {
                "date": "2014-10-15-15-18-42",
                "occurrence": 1,
                "in_response_to": ["african or european?"],
                "name": "user"
            },
            "african or european?": {
                "date": "2014-10-15-15-18-41",
                "in_response_to": ["How do know so much about swallows?"],
                "occurrence": 1,
                "name": "user"
            },
            "How do know so much about swallows?": {
                "date": "2014-10-15-15-18-40",
                "in_response_to": [],
                "name": "user",
                "occurrence": 1
            },
            "Siri is my cat": {
                "date": "2014-10-15-15-18-42",
                "occurrence": 1,
                "in_response_to": ["Who is Seri?"],
                "name": "user"
            },
            "Who is Seri?": {
                "date": "2014-10-15-15-18-41",
                "in_response_to": ["Siri is adorable"],
                "occurrence": 1,
                "name": "user"
            },
            "Siri is adorable": {
                "date": "2014-10-15-15-18-40",
                "in_response_to": [],
                "name": "user",
                "occurrence": 1
            },
            "What... is your quest?": {
                "date": "2014-10-15-15-17-31",
                "occurrence": 1,
                "in_response_to": ["To seek the Holy Grail."],
                "name": "Bridgekeeper"
            },
            "To seek the Holy Grail.": {
                "date": "2014-10-15-15-17-32",
                "in_response_to": ["What... is your quest?"],
                "occurrence": 1,
                "name": "Sir Lancelot"
            },
            "What... is your favourite colour?": {
                "date": "2014-10-15-15-17-33",
                "in_response_to": ["To seek the Holy Grail."],
                "occurrence": 1,
                "name": "Bridgekeeper"
            },
            "Blue.": {
                "date": "2014-10-15-15-17-34",
                "in_response_to": ["What... is your favourite colour?"],
                "name": "Sir Lancelot",
                "occurrence": 1
            }
        }

        self.chatbot = ChatBot("Test Bot")

        log1 = open(self.chatbot.database.path, "w+")
        log1.write(json.dumps(data))
        log1.close()

    def tearDown(self):
        """
        Remove the log files that were created for testing.
        """
        import os

        os.remove(self.chatbot.database.path)
