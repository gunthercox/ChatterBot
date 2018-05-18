===================
ChatterBot Tutorial
===================

This tutorial will guide you through the process of creating a simple command-line chat bot using ChatterBot.

Getting help
============

If you’re having trouble with this tutorial, you can post a message on Gitter_
to chat with other ChatterBot users who might be able to help.

You can also `ask questions`_ on `Stack Overflow`_ under the ``chatterbot`` tag.

If you believe that you have encountered an error in ChatterBot, please open a
ticket on GitHub: https://github.com/gunthercox/ChatterBot/issues/new

Installing ChatterBot
=====================

You can install ChatterBot on your system using Python's pip command.

.. code-block:: bash

   pip install chatterbot

See :ref:`Installation` for alternative installation options.

Creating your first chat bot
============================

Create a new file named `chatbot.py`.
Then open `chatbot.py` in your editor of choice.

Before we do anything else, ChatterBot needs to be imported.
The import for ChatterBot should look like the following line.

.. code-block:: python

   from chatterbot import ChatBot

Create a new instance of the :code:`ChatBot` class.

.. code-block:: python

   bot = ChatBot('Norman')

This line of code has created a new chat bot named `Norman`.
There is a few more parameters that we will want to specify
before we run our program for the first time.

Setting the storage adapter
---------------------------

ChatterBot comes with built in adapter classes that allow it to connect
to different types of databases. In this tutorial, we will be using the
:code:`SQLStorageAdapter` which allows the chat bot to connect to SQL databases.
By default, this adapter will create a `SQLite`_ database.

The :code:`database` parameter is used to specify the path to the database
that the chat bot will use. For this example we will call the database
`database.sqlite3`. this file will be created automatically if it doesn't
already exist.

.. code-block:: python

   bot = ChatBot(
       'Norman',
       storage_adapter='chatterbot.storage.SQLStorageAdapter',
       database='./database.sqlite3'
   )

.. note::

   The SQLStorageAdapter is ChatterBot's default adapter.
   If you do not specify an adapter in your constructor,
   the SQLStorageAdapter adapter will be used automatically.

Input and output adapters
-------------------------

Next, we will add in parameters to specify the input and output terminal
adapter. The input terminal adapter simply reads the user's input from
the terminal. The output terminal adapter prints the chat bot's response.

.. code-block:: python

   bot = ChatBot(
       'Norman',
       storage_adapter='chatterbot.storage.SQLStorageAdapter',
       input_adapter='chatterbot.input.TerminalAdapter',
       output_adapter='chatterbot.output.TerminalAdapter',
       database='./database.sqlite3'
   )

Specifying logic adapters
-------------------------

The `logic_adapters` parameter is a list of logic adapters.
In ChatterBot, a logic adapter is a class that takes an input statement
and returns a response to that statement.

You can choose to use as many logic adapters as you would like.
In this example we will use two logic adapters. The TimeLogicAdapter returns
the current time when the input statement asks for it.
The MathematicalEvaluation adapter solves math problems that use basic
operations.

.. code-block:: python

   bot = ChatBot(
       'Norman',
       storage_adapter='chatterbot.storage.SQLStorageAdapter',
       input_adapter='chatterbot.input.TerminalAdapter',
       output_adapter='chatterbot.output.TerminalAdapter',
       logic_adapters=[
           'chatterbot.logic.MathematicalEvaluation',
           'chatterbot.logic.TimeLogicAdapter'
       ],
       database='./database.sqlite3'
   )

Getting a response from your chat bot
-------------------------------------

Next, you will want to create a while loop for your chat bot to run in.
By breaking out of the loop when specific exceptions are triggered,
we can exit the loop and stop the program when a user enters `ctrl+c`.

.. code-block:: python

   while True:
       try:
           bot_input = bot.get_response(None)

       except(KeyboardInterrupt, EOFError, SystemExit):
           break

Training your chat bot
----------------------

At this point your chat bot, Norman will learn to communicate as you talk to him.
You can speed up this process by training him with examples of existing conversations.

.. code-block:: python

   bot.train([
       'How are you?',
       'I am good.',
       'That is good to hear.',
       'Thank you',
       'You are welcome.',
   ])

You can run the training process multiple times to reinforce preferred responses
to particular input statements. You can also run the train command on a number
of different example dialogs to increase the breadth of inputs that your chat
bot can respond to.

---- 

This concludes this ChatterBot tutorial. Please see other sections of the
documentation for more details and examples.

Up next: :doc:`./examples`

.. _Gitter: https://gitter.im/chatterbot/Lobby
.. _SQLite: https://www.sqlite.org/
.. _`Stack Overflow`: https://stackoverflow.com/questions/tagged/chatterbot
.. _`ask questions`: https://stackoverflow.com/questions/ask
