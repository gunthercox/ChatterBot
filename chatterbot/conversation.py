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

        self.text = text
        self.tags = kwargs.pop('tags', [])
        self.in_response_to = kwargs.pop('in_response_to', [])
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

    def add_response(self, response):
        """
        Add the response to the list of statements that this statement is in response to.
        If the response is already in the list, increment the occurrence count of that response.

        :param response: The response to add.
        :type response: `Response`
        """
        if not isinstance(response, Response):
            raise Statement.InvalidTypeException(
                'A {} was received when a {} instance was expected'.format(
                    type(response),
                    type(Response(''))
                )
            )

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

        :param response_text: The text of the response to be removed.
        :type response_text: str
        """
        for response in self.in_response_to:
            if response_text == response.text:
                self.in_response_to.remove(response)
                return True
        return False

    def get_response_count(self, statement):
        """
        Find the number of times that the statement has been used
        as a response to the current statement.

        :param statement: The statement object to get the count for.
        :type statement: `Statement`

        :returns: Return the number of times the statement has been used as a response.
        :rtype: int
        """
        for response in self.in_response_to:
            if statement.text == response.text:
                return response.occurrence

        return 0

    def serialize(self):
        """
        :returns: A dictionary representation of the statement object.
        :rtype: dict
        """
        data = {
            'text': self.text,
            'in_response_to': [],
            'extra_data': self.extra_data
        }

        for response in self.in_response_to:
            data['in_response_to'].append(response.serialize())

        return data

    @property
    def response_statement_cache(self):
        """
        This property is to allow ChatterBot Statement objects to
        be swappable with Django Statement models.
        """
        return self.in_response_to

    class InvalidTypeException(Exception):

        def __init__(self, value='Received an unexpected value type.'):
            self.value = value

        def __str__(self):
            return repr(self.value)


class Response(object):
    """
    A response represents an entity which response to a statement.
    """

    def __init__(self, text, **kwargs):
        from datetime import datetime
        from dateutil import parser as date_parser

        self.text = text
        self.conversation = kwargs.get('conversation', '')
        self.created_at = kwargs.get('created_at', datetime.now())
        self.occurrence = kwargs.get('occurrence', 1)

        if not isinstance(self.created_at, datetime):
            self.created_at = date_parser.parse(self.created_at)

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
        return {
            'text': self.text,
            'created_at': self.created_at.isoformat(),
            'conversation': self.conversation,
            'occurrence': self.occurrence
        }
