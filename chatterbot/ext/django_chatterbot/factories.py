"""
These factories are used to generate fake data for testing.
"""
import factory
from chatterbot.ext.django_chatterbot import models
from chatterbot import constants
from factory.django import DjangoModelFactory


class StatementFactory(DjangoModelFactory):

    text = factory.Faker(
        'text',
        max_nb_chars=constants.STATEMENT_TEXT_MAX_LENGTH
    )

    class Meta:
        model = models.Statement


class ResponseFactory(DjangoModelFactory):

    statement = factory.SubFactory(StatementFactory)

    response = factory.SubFactory(StatementFactory)

    class Meta:
        model = models.Response


class ConversationFactory(DjangoModelFactory):

    class Meta:
        model = models.Conversation


class TagFactory(DjangoModelFactory):

    name = factory.Faker('word')

    class Meta:
        model = models.Tag
