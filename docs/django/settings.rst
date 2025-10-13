==========================
ChatterBot Django Settings
==========================

You can edit the ChatterBot configuration through your Django settings.py file.

.. code-block:: python
   :caption: settings.py

   CHATTERBOT = {
       'name': 'Tech Support Bot',
       'logic_adapters': [
           'chatterbot.logic.MathematicalEvaluation',
           'chatterbot.logic.TimeLogicAdapter',
           'chatterbot.logic.BestMatch'
       ]
   }

Any setting that gets set in the CHATTERBOT dictionary will be passed to the chat bot that powers your django app.

Additional Django settings
==========================

- ``django_app_name`` [default: 'django_chatterbot'] The Django app name to look up the models from.
- ``database`` [default: 'default'] The Django database alias to use for ChatterBot data storage.

Swappable Model Settings
=========================

ChatterBot supports custom Statement and Tag models similar to Django's ``AUTH_USER_MODEL`` pattern:

- ``CHATTERBOT_STATEMENT_MODEL`` [default: 'django_chatterbot.Statement'] The Statement model to use.
- ``CHATTERBOT_TAG_MODEL`` [default: 'django_chatterbot.Tag'] The Tag model to use.

.. code-block:: python
   :caption: settings.py

   # Use custom models
   CHATTERBOT_STATEMENT_MODEL = 'myapp.CustomStatement'
   CHATTERBOT_TAG_MODEL = 'myapp.CustomTag'

These settings can be overridden per ChatBot instance using the ``statement_model`` and 
``tag_model`` kwargs on the storage adapter. See :doc:`custom-models` for details.

.. code-block:: python
   :caption: Per-instance configuration

   from chatterbot import ChatBot

   bot = ChatBot(
       'My Bot',
       storage_adapter='chatterbot.storage.DjangoStorageAdapter',
       statement_model='myapp.CustomStatement',
       tag_model='myapp.CustomTag'
   )

Using a Secondary Database
===========================

ChatterBot can store its data in a separate database from your main Django application. This is useful for:

- **Data isolation** - Separate backups and maintenance schedules
- **Performance** - Reduce load on your main application database
- **Organization** - Clear separation between conversational data and application data
- **Scalability** - Different database engines or servers for different needs

Configuration
-------------

1. Define your databases in ``settings.py``:

.. code-block:: python
   :caption: settings.py

   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.sqlite3',
           'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
       },
       'chatbot_db': {
           'ENGINE': 'django.db.backends.sqlite3',
           'NAME': os.path.join(BASE_DIR, 'chatbot.sqlite3'),
       }
   }

2. Configure ChatterBot to use the secondary database:

.. code-block:: python
   :caption: settings.py

   CHATTERBOT = {
       'name': 'Tech Support Bot',
       'storage_adapter': 'chatterbot.storage.DjangoStorageAdapter',
       'database': 'chatbot_db',  # Specify the database alias
       'logic_adapters': [
           'chatterbot.logic.BestMatch'
       ]
   }

3. Run migrations on the secondary database:

.. code-block:: bash

   python manage.py migrate --database=chatbot_db

ChatterBot will now utilize the secondary database to store and query its data.

Example with PostgreSQL
-----------------------

You can use different database engines for your main app and ChatterBot:

.. code-block:: python
   :caption: settings.py

   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'myapp_db',
           'USER': 'myuser',
           'PASSWORD': 'mypassword',
           'HOST': 'localhost',
           'PORT': '5432',
       },
       'chatbot_db': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'chatbot_db',
           'USER': 'chatbot_user',
           'PASSWORD': 'chatbot_password',
           'HOST': 'chatbot.example.com',
           'PORT': '5432',
       }
   }

   CHATTERBOT = {
       'name': 'Support Bot',
       'storage_adapter': 'chatterbot.storage.DjangoStorageAdapter',
       'database': 'chatbot_db',
   }
