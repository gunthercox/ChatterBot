==========================
Chatterbot Django Settings
==========================

You can edit the ChatterBot configuration through your Django settings.py file.

.. code-block:: python

   CHATTERBOT = {
       'name': 'Tech Support Bot',
       'logic_adapters': [
           'chatterbot.logic.MathematicalEvaluation',
           'chatterbot.logic.TimeLogicAdapter',
           'chatterbot.logic.BestMatch'
       ],
       'trainer': 'chatterbot.trainers.ChatterBotCorpusTrainer',
       'training_data': [
            'chatterbot.corpus.english.greetings'
       ]
   }

Any setting that gets set in the CHATTERBOT dictionary will be passed to the chat bot that powers your django app.

Additional Django settings
==========================

- ``django_app_name`` [default: 'django_chatterbot'] The Django app name to look up the models from.