from chatterbot.conversation import StatementMixin
from chatterbot import constants
from django.db import models
from django.utils import timezone
from django.conf import settings
from django.apps import apps


DJANGO_APP_NAME = constants.DEFAULT_DJANGO_APP_NAME

# Default model paths for swappable models
# These can be overridden via CHATTERBOT_STATEMENT_MODEL and CHATTERBOT_TAG_MODEL settings
DEFAULT_STATEMENT_MODEL = f'{DJANGO_APP_NAME}.Statement'
DEFAULT_TAG_MODEL = f'{DJANGO_APP_NAME}.Tag'


class AbstractBaseTag(models.Model):
    """
    The abstract base tag allows other models to be created
    using the attributes that exist on the default models.
    """

    name = models.SlugField(
        max_length=constants.TAG_NAME_MAX_LENGTH,
        unique=True,
        help_text='The unique name of the tag.'
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class AbstractBaseStatement(models.Model, StatementMixin):
    """
    The abstract base statement allows other models to be created
    using the attributes that exist on the default models.
    """

    text = models.CharField(
        max_length=constants.STATEMENT_TEXT_MAX_LENGTH,
        help_text='The text of the statement.'
    )

    search_text = models.CharField(
        max_length=constants.STATEMENT_TEXT_MAX_LENGTH,
        blank=True,
        help_text='A modified version of the statement text optimized for searching.'
    )

    conversation = models.CharField(
        max_length=constants.CONVERSATION_LABEL_MAX_LENGTH,
        help_text='A label used to link this statement to a conversation.'
    )

    created_at = models.DateTimeField(
        default=timezone.now,
        help_text='The date and time that the statement was created at.'
    )

    in_response_to = models.CharField(
        max_length=constants.STATEMENT_TEXT_MAX_LENGTH,
        null=True,
        help_text='The text of the statement that this statement is in response to.'
    )

    search_in_response_to = models.CharField(
        max_length=constants.STATEMENT_TEXT_MAX_LENGTH,
        blank=True,
        help_text='A modified version of the in_response_to text optimized for searching.'
    )

    persona = models.CharField(
        max_length=constants.PERSONA_MAX_LENGTH,
        help_text='A label used to link this statement to a persona.'
    )

    tags = models.ManyToManyField(
        settings.CHATTERBOT_TAG_MODEL if hasattr(
            settings, 'CHATTERBOT_TAG_MODEL'
        ) else DEFAULT_TAG_MODEL,
        related_name='statements',
        help_text='The tags that are associated with this statement.'
    )

    # This is the confidence with which the chat bot believes
    # this is an accurate response. This value is set when the
    # statement is returned by the chat bot.
    confidence = 0

    class Meta:
        abstract = True
        indexes = [
            models.Index(
                fields=['search_text'],
                name='idx_cb_search_text'
            ),
            models.Index(
                fields=['search_in_response_to'], name='idx_cb_search_in_response_to'
            ),
        ]

    def __str__(self):
        if len(self.text.strip()) > 60:
            return '{}...'.format(self.text[:57])
        elif len(self.text.strip()) > 0:
            return self.text
        return '<empty>'

    @classmethod
    def get_tag_model(cls):
        """
        Return the Tag model class, respecting the swappable setting.

        This method checks:
        1. Django settings (CHATTERBOT_TAG_MODEL) - project-wide configuration
        2. The model referenced by the 'tags' field - handles custom models via kwargs
        3. Falls back to DEFAULT_TAG_MODEL if introspection fails

        This ensures the correct Tag model is used even when custom models
        are specified via storage adapter kwargs rather than Django settings.
        """
        tag_model_path = getattr(settings, 'CHATTERBOT_TAG_MODEL', None)

        if tag_model_path:
            return apps.get_model(tag_model_path)

        # If no setting, infer from the ManyToManyField relationship for
        # cases where custom models are specified via kwargs
        try:
            # Get the model that this class's 'tags' field points to
            tags_field = cls._meta.get_field('tags')
            related_model = tags_field.related_model

            # Resolve strings (lazy references)
            if isinstance(related_model, str):
                return apps.get_model(related_model)
            return related_model
        except Exception:
            # Fallback to default if introspection fails
            return apps.get_model(DEFAULT_TAG_MODEL)

    def get_tags(self) -> list[str]:
        """
        Return the list of tags for this statement.
        """
        return list(self.tags.values_list('name', flat=True))

    def add_tags(self, *tags):
        """
        Add a list of strings to the statement as tags.
        """
        TagModel = self.get_tag_model()

        for tag_name in tags:
            tag_obj, _created = TagModel.objects.get_or_create(name=tag_name)
            self.tags.add(tag_obj)
