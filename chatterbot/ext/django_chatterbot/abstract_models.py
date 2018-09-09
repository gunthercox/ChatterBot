from chatterbot.conversation import StatementMixin
from chatterbot import constants
from django.db import models
from django.utils import timezone
from django.conf import settings


DJANGO_APP_NAME = constants.DEFAULT_DJANGO_APP_NAME
STATEMENT_MODEL = 'Statement'

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


class AbstractBaseStatement(models.Model, StatementMixin):
    """
    The abstract base statement allows other models to
    be created using the attributes that exist on the
    default models.
    """

    text = models.CharField(
        max_length=constants.STATEMENT_TEXT_MAX_LENGTH,
        blank=False,
        null=False
    )

    conversation = models.CharField(
        max_length=constants.CONVERSATION_LABEL_MAX_LENGTH
    )

    created_at = models.DateTimeField(
        default=timezone.now,
        help_text='The date and time that the statement was created at.'
    )

    in_response_to = models.CharField(
        max_length=constants.STATEMENT_TEXT_MAX_LENGTH,
        null=True
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

    def serialize(self):
        """
        :returns: A dictionary representation of the statement object.
        :rtype: dict
        """
        import json

        if not self.extra_data:
            self.extra_data = '{}'

        return {
            'id': self.id,
            'text': self.text,
            'in_response_to': self.in_response_to,
            'conversation': self.conversation,
            'created_at': self.created_at.isoformat().split('+', 1)[0],
            'extra_data': json.loads(self.extra_data),
        }


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
