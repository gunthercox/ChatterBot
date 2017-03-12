"""
These factories are used to generate fake data for testing.
"""
from factory.django import DjangoModelFactory
from factory import fuzzy


class StatementFactory(DjangoModelFactory):

    text = fuzzy.FuzzyText(length=50)

    class Meta:
        model = 'chatterbot.ext.django_chatterbot.Statement'


class ConversationFactory(DjangoModelFactory):

    class Meta:
        model = 'chatterbot.ext.django_chatterbot.Conversation'
