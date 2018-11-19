from pytz import UTC
from datetime import datetime
from dateutil import parser as date_parser


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

    def add_tags(self, *tags):
        """
        Add a list of strings to the statement as tags.
        """
        self.tags.extend(tags)

    def serialize(self):
        """
        :returns: A dictionary representation of the statement object.
        :rtype: dict
        """
        return {
            'id': self.id,
            'text': self.text,
            'search_text': self.search_text,
            'created_at': self.created_at.isoformat().split('+', 1)[0],
            'conversation': self.conversation,
            'in_response_to': self.in_response_to,
            'search_in_response_to': self.search_in_response_to,
            'persona': self.persona,
            'tags': self.get_tags()
        }


class Statement(StatementMixin):
    """
    A statement represents a single spoken entity, sentence or
    phrase that someone can say.
    """

    __slots__ = (
        'id',
        'text',
        'search_text',
        'conversation',
        'persona',
        'tags',
        'in_response_to',
        'search_in_response_to',
        'created_at',
        'confidence',
        'storage',
    )

    def __init__(self, text, in_response_to=None, **kwargs):

        self.id = kwargs.get('id')
        self.text = str(text)
        self.search_text = kwargs.get('search_text', '')
        self.conversation = kwargs.get('conversation', '')
        self.persona = kwargs.get('persona', '')
        self.tags = kwargs.pop('tags', [])
        self.in_response_to = in_response_to
        self.search_in_response_to = kwargs.get('search_in_response_to', '')
        self.created_at = kwargs.get('created_at', datetime.now())

        if not isinstance(self.created_at, datetime):
            self.created_at = date_parser.parse(self.created_at)

        # Set timezone to UTC if no timezone was provided
        if not self.created_at.tzinfo:
            self.created_at = self.created_at.replace(tzinfo=UTC)

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
        in_response_to = self.in_response_to or ''
        return hash(self.text + ':' + in_response_to)

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
