=================
Quick Start Guide
=================

Create a new chat bot
=====================

.. code-block:: python

   from chatterbot import ChatBot
   chatbot = ChatBot("Ron Obvious")

.. note::

   The only required parameter for the `ChatBot` is a name.
   This can be any anything you want.

Training
========

After creating a new ChatterBot instance it is also possible to train the bot.
Training is a good way to ensure that the bot starts off with knowledge about
specific responses. The current training method takes a list of statements that
represent a conversation.
Additional notes on training can be found in the :ref:`Training <set_trainer>` documentation.

.. note::

   Training is not required but it is recommended.

.. code-block:: python

   from chatterbot.trainers import ListTrainer

   conversation = [
       "Hello",
       "Hi there!",
       "How are you doing?",
       "I'm doing great.",
       "That is good to hear",
       "Thank you.",
       "You're welcome."
   ]

   chatbot.set_trainer(ListTrainer)
   chatbot.train(conversation)

Get a response
==============

.. code-block:: python

   response = chatbot.get_response("Good morning!")
   print(response)

Read only mode
==============

Your ChatterBot will learn based on each new input statement it receives.
If you want to disable this learning feature after your bot has been trained,
you can set `read_only=True` as a parameter when initializing the bot.

.. code-block:: python

   chatbot = ChatBot("Johnny Five", read_only=True)
