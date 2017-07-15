from django.db import models
from django.utils import timezone


class AbstractBasePhrase(models.Model):
    """
    A small group of words representing a conceptual unit.
    """

    text = models.CharField(
        # unique=True,
        blank=True,
        null=False,
        max_length=255
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.text

class AbstractBaseStatement(models.Model):
    """
    The abstract base statement allows other models to
    be created using the attributes that exist on the
    default models.
    """

    text = models.CharField(
        blank=False,
        null=False,
        max_length=255
    )

    phrase = models.ForeignKey(
        'Phrase',
        related_name='statements',
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        default=timezone.now,
        help_text='The date and time that this statement was created at.'
    )

    extra_data = models.CharField(max_length=500)

    # This is the confidence with which the chat bot believes
    # this is an accurate response. This value is set when the
    # statement is returned by the chat bot.
    confidence = 0

    class Meta:
        abstract = True

    def __str__(self):
        if len(self.text.strip()) > 60:
            return '{}...'.format(self.text[:57])
        elif len(self.text.strip()) > 0:
            return self.text
        return '<empty>'

    def __init__(self, *args, **kwargs):
        super(AbstractBaseStatement, self).__init__(*args, **kwargs)

        # Responses to be saved if the statement is updated with the storage adapter
        self.response_statement_cache = []

    @property
    def in_response_to(self):
        """
        Return the response objects that are for this statement.
        """
        return Response.objects.filter(statement=self)

    def add_extra_data(self, key, value):
        """
        Add extra data to the extra_data field.
        """
        import json

        if not self.extra_data:
            self.extra_data = '{}'

        extra_data = json.loads(self.extra_data)
        extra_data[key] = value

        self.extra_data = json.dumps(extra_data)

    def add_response(self, statement):
        """
        Add a response to this statement.
        """
        self.response_statement_cache.append(statement)

    def remove_response(self, response_text):
        """
        Removes a response from the statement's response list based
        on the value of the response text.

        :param response_text: The text of the response to be removed.
        :type response_text: str
        """
        is_deleted = False
        response = self.in_response.filter(response__text=response_text)

        if response.exists():
            is_deleted = True

        return is_deleted

    def get_response_count(self, statement):
        """
        Find the number of times that the statement has been used
        as a response to the current statement.

        :param statement: The statement object to get the count for.
        :type statement: chatterbot.conversation.statement.Statement

        :returns: Return the number of times the statement has been used as a response.
        :rtype: int
        """
        try:
            response = self.in_response.get(response__text=statement.text)
            return response.occurrence
        except Response.DoesNotExist:
            return 0

    def serialize(self):
        """
        :returns: A dictionary representation of the statement object.
        :rtype: dict
        """
        import json
        data = {}

        if not self.extra_data:
            self.extra_data = '{}'

        data['text'] = self.text
        data['in_response_to'] = []
        data['created_at'] = self.created_at
        data['extra_data'] = json.loads(self.extra_data)

        for response in self.in_response.all():
            data['in_response_to'].append(response.serialize())

        return data


class AbstractBaseResponse(models.Model):
    """
    The abstract base response allows other models to
    be created using the attributes that exist on the
    default models.
    """

    statement = models.ForeignKey(
        'Statement',
        related_name='in_response'
    )

    response = models.ForeignKey(
        'Statement',
        related_name='responses'
    )

    unique_together = (('statement', 'response'),)

    occurrence = models.PositiveIntegerField(default=1)

    created_at = models.DateTimeField(
        default=timezone.now,
        help_text='The date and time that this response was created at.'
    )

    class Meta:
        abstract = True

    def __str__(self):
        statement = self.statement.text
        response = self.response.text
        return '{} => {}'.format(
            statement if len(statement) <= 20 else statement[:17] + '...',
            response if len(response) <= 40 else response[:37] + '...'
        )

    def serialize(self):
        """
        :returns: A dictionary representation of the statement object.
        :rtype: dict
        """
        data = {}

        data['text'] = self.response.text
        data['created_at'] = self.created_at.isoformat()
        data['occurrence'] = self.occurrence

        return data


class AbstractBaseConversation(models.Model):
    """
    The abstract base conversation allows other models to
    be created using the attributes that exist on the
    default models.
    """

    statements = models.ManyToManyField(
        'Phrase',
        related_name='conversations',
        help_text='The phrases in this conversation.'
    )

    class Meta:
        abstract = True

    def __str__(self):
        return str(self.id)


class Statement(AbstractBaseStatement):
    """
    A statement represents a single spoken entity, sentence or
    phrase that someone can say.
    """
    pass


class Response(AbstractBaseResponse):
    """
    Connection between a response and the statement that triggered it.

    Comparble to a ManyToMany "through" table, but without the M2M indexing/relations.
    The text and number of times the response has occurred are stored.
    """
    pass


class Conversation(AbstractBaseConversation):
    """
    A sequence of statements representing a conversation.
    """
    pass


class Phrase(AbstractBasePhrase):
    """
    A small group of words representing a conceptual unit.
    """
    pass