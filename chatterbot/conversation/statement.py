from .signature import Signature


class Statement(object):

    def __init__(self, text, **kwargs):
        self.text = text

        self.signatures = kwargs.get("signatures", [])
        self.in_response_to = kwargs.get("in_response_to", [])

        self.modified = False

    def __str__(self):
        return self.text

    def __repr__(self):
        return "<Statement text:%s>" % (self.text)

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
        updated = False
        for index in range(0, len(self.in_response_to)):
            if statement.text == self.in_response_to[index].text:
                self.in_response_to[index].occurrence += 1
                updated = True

        if not updated:
            self.in_response_to.append(
                Response(statement.text)
            )

    def get_response_count(self, statement):
        """
        Return the number of times the statement occurs in the database.
        """
        for response in self.in_response_to:
            if statement.text == response.text:
                return response.occurrence

        return 0

    def add_signature(self, signature):
        self.signatures.append(signature)

    def serialize(self):
        """
        Returns a dictionary representation of the current object.
        """
        data = {}

        data["text"] = self.text
        data["in_response_to"] = []

        for response in self.in_response_to:
            data["in_response_to"].append(
                [response.text, response.occurrence]
            )

        data["signature"] = []

        for signature in self.signatures:
            data["signature"].append(signature.serialize())

        return data


class Response(object):

    def __init__(self, text, **kwargs):
        self.text = text
        self.occurrence = kwargs.get("occurrence", 1)

    def __str__(self):
        return self.text

    def __repr__(self):
        return "<Response text:%s>" % (self.text)

    def __eq__(self, other):
        if not other:
            return False

        if isinstance(other, Response):
            return self.text == other.text

        if isinstance(other, Statement):
            return self.text == other.text

        return self.text == other

