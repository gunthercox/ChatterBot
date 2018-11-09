=================
Quick Start Guide
=================

The first thing you'll need to do to get started is install ChatterBot.

.. code-block:: bash

   pip install chatterbot

See :ref:`Installation` for options for alternative installation methods.

Create a new chat bot
=====================

.. code-block:: python

   from chatterbot import ChatBot
   chatbot = ChatBot("Ron Obvious")

.. note::

   The only required parameter for the `ChatBot` is a name.
   This can be anything you want.

Training your ChatBot
=====================

After creating a new ChatterBot instance it is also possible to train the bot.
Training is a good way to ensure that the bot starts off with knowledge about
specific responses. The current training method takes a list of statements that
represent a conversation.
Additional notes on training can be found in the :ref:`Training` documentation.

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

   trainer = ListTrainer(chatbot)

   trainer.train(conversation)

Get a response
==============

.. code-block:: python

   response = chatbot.get_response("Good morning!")
   print(response)
