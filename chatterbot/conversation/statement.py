from .signature import Signature


class Statement(object):

    def __init__(self, text, **kwargs):
        self.text = text
        self.in_response_to = kwargs.get("in_response_to", [])

        self.extra_data = {}

        if "in_response_to" in kwargs:
            del(kwargs["in_response_to"])

        self.extra_data.update(kwargs)

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

    def add_extra_data(self, key, value):
        self.extra_data[key] = value

    def add_response(self, response):
        """
        Add the response to the list if it does not already exist.
        """
        updated = False
        for index in range(0, len(self.in_response_to)):
            if response.text == self.in_response_to[index].text:
                self.in_response_to[index].occurrence += 1
                updated = True

        if not updated:
            self.in_response_to.append(response)

    def remove_response(self, response_text):
        """
        Removes a response from the statement's response list based
        on the value of the response text.
        """
        for response in self.in_response_to:
            if response_text == response.text:
                self.in_response_to.remove(response)
                return True
        return False

    def get_response_count(self, statement):
        """
        Return the number of times the statement occurs in the database.
        """
        for response in self.in_response_to:
            if statement.text == response.text:
                return response.occurrence

        return 0

    def serialize(self):
        """
        Returns a dictionary representation of the current object.
        """
        data = {}

        data["text"] = self.text
        data["in_response_to"] = []
        data.update(self.extra_data)

        for response in self.in_response_to:
            data["in_response_to"].append(response.serialize())

        return data


class Response(object):

    def __init__(self, text, **kwargs):
        self.text = text
        self.occurrence = kwargs.get("occurrence", 1)
        self.signatures = kwargs.get("signatures", [])

    def __str__(self):
        return self.text

    def __repr__(self):
        return "<Response text:%s>" % (self.text)

    def __eq__(self, other):
        if not other:
            return False

        if isinstance(other, Response):
            return self.text == other.text

        return self.text == other

    def add_signature(self, signature):
        self.signatures.append(signature)

    def serialize(self):
        data = {}

        data["text"] = self.text
        data["occurrence"] = self.occurrence
        data["signature"] = []

        for signature in self.signatures:
            data["signature"].append(signature.serialize())

        return data
