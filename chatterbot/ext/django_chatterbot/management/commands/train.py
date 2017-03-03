from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """
    A Django management command for calling a
    chat bot's training method.
    """

    help = 'Trains the database used by the chat bot'
    can_import_settings = True

    def handle(self, *args, **options):
        from chatterbot import ChatBot
        from chatterbot.ext.django_chatterbot import settings

        chatterbot = ChatBot(**settings.CHATTERBOT)

        chatterbot.train(chatterbot.training_data)

        # Django 1.8 does not define SUCCESS
        if hasattr(self.style, 'SUCCESS'):
            style = self.style.SUCCESS
        else:
            style = self.style.NOTICE

        training_class = chatterbot.trainer.__class__.__name__
        self.stdout.write(style('ChatterBot trained using "%s"' % training_class))
