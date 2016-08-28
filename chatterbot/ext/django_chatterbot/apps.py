from django.apps import AppConfig
from chatterbot.ext.django_chatterbot import settings as chatterbot_settings


class DjangoChatterbotConfig(AppConfig):

    name = 'chatterbot.ext.django_chatterbot'
    verbose_name = 'Django ChatterBot'

    def ready(self):
        chatterbot_settings.patch_all()
