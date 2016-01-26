from chatterbot.adapters import Adapter
from chatterbot.adapters.exceptions import AdapterNotImplementedError


class ClassifierAdapter(Adapter):
    """
    This is an abstract class that represents the interface
    that all classifier logic adapters should implement.
    """

    def train(self, training_data):
        """
        Data is given to train the classifier to respond to
        specific statements.
        """
        raise AdapterNotImplementedError()

    def classify(self, statement):
        """
        Method that takes an input statement and returns
        a confidence value as output.
        """
        raise AdapterNotImplementedError()
