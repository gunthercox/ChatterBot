"""
Default ChatterBot settings for Django.
"""
from django.conf import settings


CHATTERBOT_SETTINGS = getattr(settings, 'CHATTERBOT', {})

CHATTERBOT_DEFAULTS = {
    'name': 'ChatterBot',
    'storage_adapter': 'chatterbot.storage.DjangoStorageAdapter',
    'input_adapter': 'chatterbot.input.VariableInputTypeAdapter',
    'output_adapter': 'chatterbot.output.OutputAdapter',
    'use_django_models': True
}

CHATTERBOT = CHATTERBOT_DEFAULTS.copy()
CHATTERBOT.update(CHATTERBOT_SETTINGS)
