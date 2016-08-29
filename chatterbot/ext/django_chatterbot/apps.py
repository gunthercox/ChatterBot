from django.apps import AppConfig


class DjangoChatterBotConfig(AppConfig):

    name = 'chatterbot.ext.django_chatterbot'
    label = 'django_chatterbot'
    verbose_name = 'Django ChatterBot'

    def ready(self):
        from chatterbot.ext.django_chatterbot import settings
        settings.patch_all()
