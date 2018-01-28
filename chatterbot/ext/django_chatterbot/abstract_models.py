from chatterbot.conversation import StatementMixin
from chatterbot import constants
from django.db import models
from django.apps import apps
from django.utils import timezone
from django.conf import settings


DJANGO_APP_NAME = constants.DEFAULT_DJANGO_APP_NAME
STATEMENT_MODEL = 'Statement'
RESPONSE_MODEL = 'Response'

if hasattr(settings, 'CHATTERBOT'):
    """
    Allow related models to be overridden in the project settings.
    Default to the original settings if one is not defined.
    """
    DJANGO_APP_NAME = settings.CHATTERBOT.get(
        'django_app_name',
        DJANGO_APP_NAME
    )
    STATEMENT_MODEL = settings.CHATTERBOT.get(
        'statement_model',
        STATEMENT_MODEL
    )
    RESPONSE_MODEL = settings.CHATTERBOT.get(
        'response_model',
        RESPONSE_MODEL
    )


class AbstractBaseStatement(models.Model, StatementMixin):
    """
    The abstract base statement allows other models to
    be created using the attributes that exist on the
    default models.
    """

    text = models.CharField(
        unique=True,
        blank=False,
        null=False,
        max_length=constants.STATEMENT_TEXT_MAX_LENGTH
    )

    extra_data = models.CharField(
        max_length=500,
        blank=True
    )

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
        ResponseModel = apps.get_model(DJANGO_APP_NAME, RESPONSE_MODEL)
        return ResponseModel.objects.filter(statement=self)

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

    def add_tags(self, tags):
        """
        Add a list of strings to the statement as tags.
        (Overrides the method from StatementMixin)
        """
        for tag in tags:
            self.tags.create(
                name=tag
            )

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
        :type statement: chatterbot.conversation.Statement

        :returns: Return the number of times the statement has been used as a response.
        :rtype: int
        """
        return self.in_response.filter(response__text=statement.text).count()

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
        STATEMENT_MODEL,
        related_name='in_response',
        on_delete=models.CASCADE
    )

    response = models.ForeignKey(
        STATEMENT_MODEL,
        related_name='responses',
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(
        default=timezone.now,
        help_text='The date and time that this response was created at.'
    )

    class Meta:
        abstract = True

    @property
    def occurrence(self):
        """
        Return a count of the number of times this response has occurred.
        """
        ResponseModel = apps.get_model(DJANGO_APP_NAME, RESPONSE_MODEL)

        return ResponseModel.objects.filter(
            statement__text=self.statement.text,
            response__text=self.response.text
        ).count()

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

    responses = models.ManyToManyField(
        RESPONSE_MODEL,
        related_name='conversations',
        help_text='The responses in this conversation.'
    )

    class Meta:
        abstract = True

    def __str__(self):
        return str(self.id)


class AbstractBaseTag(models.Model):
    """
    The abstract base tag allows other models to
    be created using the attributes that exist on the
    default models.
    """

    name = models.SlugField(
        max_length=constants.TAG_NAME_MAX_LENGTH
    )

    statements = models.ManyToManyField(
        STATEMENT_MODEL,
        related_name='tags'
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.name
