from unittest import TestCase
from chatterbot.adapters.logic import NaiveBayes_Classifier


class NaiveBayesClassifierTests(TestCase):

    def setUp(self):
        self.adapter = NaiveBayes_Classifier()

    def test_training(self):
        training_data = [
            ("what time it is?", 1),
            ("what is the current time", 1),
            ("who am I?", 0)
        ]

        self.adapter.train(training_data)
        self.assertEqual(self.adapter.classify("what time it is?"), 1)
