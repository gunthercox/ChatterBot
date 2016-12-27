"""
Test Django settings
"""
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = 'fake-key'

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'chatterbot.ext.django_chatterbot',
    'tests_django',
]

CHATTERBOT = {
    'name': 'Test Django ChatterBot',
    'trainer': 'chatterbot.trainers.ChatterBotCorpusTrainer',
    'training_data': [
        'chatterbot.corpus.english.greetings'
    ],
    'initialize': False
}

ROOT_URLCONF = 'chatterbot.ext.django_chatterbot.urls'

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

USE_TZ = True
