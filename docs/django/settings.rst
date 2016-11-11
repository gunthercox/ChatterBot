==========================
Chatterbot Django Settings
==========================

You can edit the ChatterBot configuration through your Django settings.py file.

.. code-block:: python

   CHATTERBOT = {
       'name': 'Tech Support Bot',
       'logic_adapters': [
           'chatterbot.adapters.logic.MathematicalEvaluation',
           'chatterbot.adapters.logic.TimeLogicAdapter',
           'chatterbot.adapters.logic.ClosestMatchAdapter'
       ],
       'trainer': 'chatterbot.trainers.ChatterBotCorpusTrainer',
       'training_data': [
            'chatterbot.corpus.english.greetings'
       ]
   }

Any setting that gets set in the CHATTERBOT dictionary will be passed to the chat bot that powers your django app.
