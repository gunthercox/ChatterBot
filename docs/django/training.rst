===============
Django Training
===============

Management command
==================

When using ChatterBot with Django, the training process can be
executed by running the training management command. 

.. code-block:: bash

   python manage.py train

Training settings
=================

You can specify any data that you want to be passed to the chat bot
trainer in the :code:`training_data` parameter in your :code:`CHATTERBOT`
Django settings.

.. code-block:: python

   CHATTERBOT = {
       # ...
       'trainer': 'chatterbot.trainers.ChatterBotCorpusTrainer',
       'training_data': [
            'chatterbot.corpus.english.greetings'
       ]
   }

.. note::

   You can also specify paths to corpus files or directories of corpus files in the :code:`training_data` list.

See the documentation for the :ref:`training-classes` for other training class options that can be used here.
