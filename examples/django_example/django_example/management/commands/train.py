"""
This is an example of a custom Django management command that
trains a ChatterBot instance with specified data.

For more information on how to create custom management commands,
see the Django documentation:
https://docs.djangoproject.com/en/4.2/howto/custom-management-commands/

For details on the available training options for ChatterBot see:
http://docs.chatterbot.us/training/ 
"""

from django.core.management.base import BaseCommand
from django.conf import settings

from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer


class Command(BaseCommand):
    help = 'Train a ChatterBot instance with specified data.'

    def handle(self, *args, **options):
        chatbot = ChatBot(**settings.CHATTERBOT)

        trainer = ListTrainer(chatbot)

        trainer.train([
            'Hello, how are you?',
            'I am good.',
            'That is good to hear.',
            'I am glad to hear that.',
            'Thank you.',
            'You are welcome.',
        ])

        self.stdout.write(
            self.style.SUCCESS('Training completed successfully')
        )
