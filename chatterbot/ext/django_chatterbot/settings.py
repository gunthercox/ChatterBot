from django.conf import settings
#from chatterbot.trainers import ListTrainer

CHATTERBOT = {
    'NAME': 'ChatterBot',
#    'TRAINER': ListTrainer
}

def patch_all():
    setattr(settings, 'CHATTERBOT', CHATTERBOT)
