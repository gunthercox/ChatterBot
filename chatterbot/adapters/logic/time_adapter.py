from .logic_adapter import LogicAdapter
from chatterbot.conversation import Statement
from textblob.classifiers import NaiveBayesClassifier
from datetime import datetime


class TimeLogicAdapter(LogicAdapter):
    """
    The TimeLogicAdapter returns the current time.
    """

    def __init__(self, **kwargs):
        super(TimeLogicAdapter, self).__init__(**kwargs)

        training_data = [
            ("what time is it", 1),
            ("do you know the time", 1),
            ("do you know what time it is", 1),
            ("what is the time", 1),
            ("do you know the time", 0),
            ("it is time to go to sleep", 0),
            ("what is your favorite color", 0),
            ("i had a great time", 0),
            ("what is", 0)
        ]

        self.classifier = NaiveBayesClassifier(training_data)

    def process(self, statement):
        now = datetime.now()

        confidence = self.classifier.classify(statement.text.lower())
        response = Statement("The current time is " + now.strftime("%I:%M %p"))

        return confidence, response
