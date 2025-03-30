"""
Default ChatterBot settings for Django.
"""
from django.conf import settings
from chatterbot import constants


CHATTERBOT = getattr(settings, 'CHATTERBOT', {})

CHATTERBOT_DEFAULTS = {
    'name': 'ChatterBot',
    'storage_adapter': 'chatterbot.storage.DjangoStorageAdapter',
    'django_app_name': constants.DEFAULT_DJANGO_APP_NAME
}

CHATTERBOT.update(CHATTERBOT_DEFAULTS)
