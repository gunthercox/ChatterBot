from django.conf import settings


CHATTERBOT_SETTINGS = getattr(settings, 'CHATTERBOT', {})

CHATTERBOT_DEFAULTS = {
    'name': 'ChatterBot',
    'storage_adapter': 'chatterbot.adapters.storage.DjangoStorageAdapter',
    'input_adapter': 'chatterbot.adapters.input.VariableInputTypeAdapter',
    'output_adapter': 'chatterbot.adapters.output.OutputFormatAdapter',
    'output_format': 'json'
}

CHATTERBOT = CHATTERBOT_DEFAULTS.copy()
CHATTERBOT.update(CHATTERBOT_SETTINGS)
