from .signature import Signature


class Statement(object):

    def __init__(self, text, **kwargs):
        self.text = text
        self.occurrence = kwargs.get("occurrence", 1)

        self.signatures = kwargs.get("signatures", [])

        self.in_response_to = kwargs.get("in_response_to", [])

        self.modified = False

    def __eq__(self, other):
        if not other:
            return False

        if isinstance(other, Statement):
            return self.text == other.text

        return self.text == other

    def add_response(self, statement):
        """
        Add the statement to the list if it does not already exist.
        """
        if not statement.text in self.in_response_to:
            self.in_response_to.append(statement.text)

    def get_occurrence_count(self):
        """
        Return the number of times the statement occurs in the database.
        """
        return self.occurrence

    def update_occurrence_count(self):
        """
        Increment the occurrence count.
        """
        self.occurrence = self.occurrence + 1

    def add_signature(self, signature):
        self.signatures.append(signature)

    def serialize(self):
        """
        Returns a dictionary representation of the current object.
        """
        data = {}

        data["text"] = self.text
        data["occurrence"] = self.occurrence
        data["in_response_to"] = self.in_response_to

        data["signature"] = []

        for signature in self.signatures:
            data["signature"].append(signature.serialize())

        return data

