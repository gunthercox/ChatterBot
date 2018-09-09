class StatementMixin(object):
    """
    This class has shared methods used to
    normalize different statement models.
    """

    def get_tags(self):
        """
        Return the list of tags for this statement.
        """
        return self.tags

    def add_tags(self, tags):
        """
        Add a list of strings to the statement as tags.
        """
        for tag in tags:
            self.tags.append(tag)


class Statement(StatementMixin):
    """
    A statement represents a single spoken entity, sentence or
    phrase that someone can say.
    """

    def __init__(self, text, **kwargs):
        from datetime import datetime
        from dateutil import parser as date_parser

        # Try not to allow non-string types to be passed to statements
        try:
            text = str(text)
        except UnicodeEncodeError:
            pass

        self.id = kwargs.get('id')

        self.text = text

        self.conversation = kwargs.get('conversation', '')

        self.tags = kwargs.pop('tags', [])
        self.in_response_to = kwargs.pop('in_response_to', None)
        self.created_at = kwargs.get('created_at', datetime.now())

        if not isinstance(self.created_at, datetime):
            self.created_at = date_parser.parse(self.created_at)

        self.extra_data = kwargs.pop('extra_data', {})

        # This is the confidence with which the chat bot believes
        # this is an accurate response. This value is set when the
        # statement is returned by the chat bot.
        self.confidence = 0

        self.storage = None

    def __str__(self):
        return self.text

    def __repr__(self):
        return '<Statement text:%s>' % (self.text)

    def __hash__(self):
        return hash(self.text)

    def __eq__(self, other):
        if not other:
            return False

        if isinstance(other, Statement):
            return self.text == other.text

        return self.text == other

    def save(self):
        """
        Save the statement in the database.
        """
        self.storage.update(self)

    def add_extra_data(self, key, value):
        """
        This method allows additional data to be stored on the statement object.

        Typically this data is something that pertains just to this statement.
        For example, a value stored here might be the tagged parts of speech for
        each word in the statement text.

            - key = 'pos_tags'
            - value = [('Now', 'RB'), ('for', 'IN'), ('something', 'NN'), ('different', 'JJ')]

        :param key: The key to use in the dictionary of extra data.
        :type key: str

        :param value: The value to set for the specified key.
        """
        self.extra_data[key] = value

    def serialize(self):
        """
        :returns: A dictionary representation of the statement object.
        :rtype: dict
        """
        return {
            'id': self.id,
            'text': self.text,
            'created_at': self.created_at.isoformat().split('+', 1)[0],
            'conversation': self.conversation,
            'in_response_to': self.in_response_to,
            'extra_data': self.extra_data
        }

    class InvalidTypeException(Exception):

        def __init__(self, value='Received an unexpected value type.'):
            self.value = value

        def __str__(self):
            return repr(self.value)
