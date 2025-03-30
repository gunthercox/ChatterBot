from django.apps import AppConfig


class DjangoChatterBotConfig(AppConfig):

    name = 'chatterbot.ext.django_chatterbot'
    label = 'django_chatterbot'
    verbose_name = 'Django ChatterBot'

    def ready(self):
        from chatterbot.ext.django_chatterbot import settings as defaults
        from django.conf import settings

        settings.CHATTERBOT = getattr(settings, 'CHATTERBOT', {})
        settings.CHATTERBOT.update(defaults.CHATTERBOT_DEFAULTS)
