from django.conf import settings


CHATTERBOT = {
    'NAME': 'ChatterBot'
}

def patch_all():
    setattr(settings, 'CHATTERBOT', CHATTERBOT)
