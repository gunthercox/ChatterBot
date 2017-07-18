class Response(object):
    """
    A response represents an entity which response to a statement.
    """

    def __init__(self, text, **kwargs):
        from datetime import datetime
        self.text = text
        self.created_at = kwargs.get('created_at', datetime.now())
        self.occurrence = kwargs.get('occurrence', 1)

    def __str__(self):
        return self.text

    def __repr__(self):
        return '<Response text:%s>' % (self.text)

    def __hash__(self):
        return hash(self.text)

    def __eq__(self, other):
        if not other:
            return False

        if isinstance(other, Response):
            return self.text == other.text

        return self.text == other

    def serialize(self):
        data = {}

        data['text'] = self.text
        data['created_at'] = self.created_at
        data['occurrence'] = self.occurrence

        return data
