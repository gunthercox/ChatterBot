# -*- coding: utf-8 -*-
from datetime import datetime


class StatementModelMixin(object):

    collection_name = 'statements'

    pk_field = 'text'
    fields = (
        'text', 'created_at', 'in_response_to', 'extra_data',
    )


class StatementSerializer(object):

    def serialize(self, obj):
        """
        :returns: A dictionary representation of the statement object.
        :rtype: dict
        """
        data = {}

        data['text'] = obj.text
        if obj.in_response_to:
            data['in_response_to'] = {'text': obj.in_response_to.text}
        data['created_at'] = obj.created_at
        data['extra_data'] = obj.extra_data

        return data

    def deserialize(self, data):
        pass


class Statement(StatementModelMixin):
    """
    A statement represents a single spoken entity, sentence or
    phrase that someone can say.
    """

    storage = None

    def __init__(self, text, **kwargs):
        self.text = text
        self.in_response_to = kwargs.pop('in_response_to', None)

        # The date and time that this statement was created at
        self.created_at = kwargs.pop('created_at', datetime.now())

        self.extra_data = kwargs.pop('extra_data', {})

        # This is the confidence with which the chat bot believes
        # this is an accurate response. This value is set when the
        # statement is returned by the chat bot.
        self.confidence = 0

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
        serializer = StatementSerializer()
        return serializer.serialize(self)

    class InvalidTypeException(Exception):

        def __init__(self, value='Recieved an unexpected value type.'):
            self.value = value

        def __str__(self):
            return repr(self.value)
