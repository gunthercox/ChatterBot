from __future__ import unicode_literals
from datetime import datetime
from .logic_adapter import LogicAdapter


class TimeLogicAdapter(LogicAdapter):
    """
    The TimeLogicAdapter returns the current time.
    """

    def __init__(self, **kwargs):
        super(TimeLogicAdapter, self).__init__(**kwargs)
        from nltk import NaiveBayesClassifier

        self.positive = [
            'what time is it',
            'do you know the time',
            'do you know what time it is',
            'what is the time'
        ]

        self.negative = [
            'it is time to go to sleep',
            'what is your favorite color',
            'i had a great time',
            'what is'
        ]

        labeled_data = (
            [(name, 0) for name in self.negative] +
            [(name, 1) for name in self.positive]
        )

        # train_set = apply_features(self.time_question_features, training_data)
        train_set = [(self.time_question_features(n), text) for (n, text) in labeled_data]

        self.classifier = NaiveBayesClassifier.train(train_set)

    def time_question_features(self, text):
        """
        Provide an analysis of significan features in the string.
        """
        features = {}

        all_words = " ".join(self.positive + self.negative).split()

        for word in text.split():
            features['contains({})'.format(word)] = (word in all_words)

        for letter in 'abcdefghijklmnopqrstuvwxyz':
            features['count({})'.format(letter)] = text.lower().count(letter)
            features['has({})'.format(letter)] = (letter in text.lower())

        return features

    def process(self, statement):
        from chatterbot.conversation import Statement

        now = datetime.now()

        time_features = self.time_question_features(statement.text.lower())
        confidence = self.classifier.classify(time_features)
        response = Statement('The current time is ' + now.strftime('%I:%M %p'))

        return confidence, response
