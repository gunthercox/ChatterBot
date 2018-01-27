"""
Django settings for when tests are run.
"""
import os

DEBUG = True

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
    'show_training_progress': False,
    'logic_adapters': [
        {
            'import_path': 'chatterbot.logic.BestMatch',
        },
        {
            'import_path': 'chatterbot.logic.MathematicalEvaluation',
        }
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

# Using the MD5 password hasher improves test performance
PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.MD5PasswordHasher',
)

USE_TZ = True
