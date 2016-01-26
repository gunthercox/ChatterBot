from textblob.classifiers import NaiveBayesClassifier
from .base_classifier import ClassifierAdapter

class NaiveBayes_Classifier(ClassifierAdapter):
    def __init__(self):
        pass

    def train(self, training_data):
        """
        Data is given to train the classifier to respond to
        specific statements.
        """

        self.classifier = NaiveBayesClassifier(training_data)

    def classify(self, input_text):
        """
        Method that takes an input statement and returns
        a confidence value as output.
        """

        return self.classifier.classify(input_text.lower())
