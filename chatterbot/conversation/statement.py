import datetime


class Statement(object):

    def __init__(self, text):
        self.text = text
        self.occurrence = 0
        self.in_response_to = []
        self.signatures = []

    def now(self, fmt="%Y-%m-%d-%H-%M-%S"):
        """
        Returns a string formatted timestamp of the current time.
        """
        return datetime.datetime.now().strftime(fmt)

    def add_signature(self, name):

        signature = {}

        signature["name"] = name
        signature["time"] = self.now()

        self.signatures.append(signature)

    def serialize(self):
        """
        Returns a dictionary representation of the current object.
        """

        statement = {}

        statement["text"] = self.text
        statement["occurrence"] = self.occurrence
        statement["in_response_to"] = self.in_response_to
        statement["signatures"] = self.signatures

        return statement
