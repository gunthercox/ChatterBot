===================
ChatterBot Tutorial
===================

Installing ChatterBot
=====================

The recommended method for installing ChatterBot is by using `pip`_.
To install ChatterBot using pip run the following command in your terminal.

.. code-block:: bash

   pip install chatterbot

Creating your first chat bot
============================

Create a new file named `chatbot.py`.
Then open `chatbot.py` in your editor of choice.

Before we do anything, ChatterBot needs to be imported.
The import for ChatterBot should look like the following line.

.. code-block:: python

   from chatterbot import ChatBot

Create a new instance of the :code:`ChatBot` class.

.. code-block:: python

   bot = ChatBot('Norman')

This line of code has created a new chat bot named `Norman`.
There is a few more parameters that we will want to specify
before we run our program for the first time.

Storage adapter
---------------

ChatterBot comes with built in adapter classes that allow it to connect
to different types of databases. In this tutorial, we will be using the
`JsonFileStorageAdapter` which is a simple storage adapter that stores data
in a json formatted file on your hard disk. This functionality makes
this storage adapter very good for testing and debugging.

.. warning::

   The JsonFileStorageAdapter is not intended for use with large amounts of
   data. You may expirience serious performance problems if the size of
   this database becomes too large.

We will select the `JsonFileStorageAdapter` by specifying it in our chat
bot's constructor.

The `database` parameter is used to specify the path to the database
that the chat bot will use. For this example we will call the database
`database.json`. The `database.json` file will be created automatically
if it does not already exist.

.. code-block:: python

   bot = ChatBot(
       "Norman",
       storage_adapter="chatterbot.adapters.storage.JsonFileStorageAdapter",
       database="./database.json"
   )

.. note::

   The JsonFileStorageAdapter is ChatterBot's default adapter.
   If you do not specify an adapter in your constructor,
   the JsonDatabase adapter will be used automatically.

Input and output adapters
-------------------------

Next, we will add in parameters to specify the input and output terminal
adapter. The input terminal adapter simply reads the user's input from
the terminal. The output terminal adapter print's the chat bot's response.

.. code-block:: python

   bot = ChatBot(
       "Norman",
       storage_adapter="chatterbot.adapters.storage.JsonFileStorageAdapter",
       input_adapter="chatterbot.adapters.input.TerminalAdapter",
       output_adapter="chatterbot.adapters.output.TerminalAdapter",
       database="./database.json"
   )

Logic adapters
--------------

The `logic_adapters` parameter is a list of logic adapters.
In ChatterBot, a logic adapter is a class that take's an input statement
and returns a response to that statement.

You can choose to use as many logic adapters as you would like.
In this example we will use two logic adapters. The TimeLogicAdapter returns
the current time when the input statement asks for it.
The MathematicalEvaluation adapter solves math problems that use basic
operations.

.. code-block:: python

   bot = ChatBot(
       "Norman",
       storage_adapter="chatterbot.adapters.storage.JsonFileStorageAdapter",
       input_adapter="chatterbot.adapters.input.TerminalAdapter",
       output_adapter="chatterbot.adapters.output.TerminalAdapter",
       logic_adapters=[
           "chatterbot.adapters.logic.MathematicalEvaluation",
           "chatterbot.adapters.logic.TimeLogicAdapter"
       ],
       database="./database.json"
   )

Getting a response
------------------

Next, you will want to create a while loop for your chat bot to run in.
By breaking out of the loop when specific exceptions are triggered,
we can exit the loop and stop the program when a user enters `ctrl+c`.

.. code-block:: python

   while True:
       try:
        bot_input = bot.get_response(None)

       except(KeyboardInterrupt, EOFError, SystemExit):
           break

This concludes this ChatterBot tutorial. Please see other sections of the
documentation for more details and examples.

Next: See :doc:`./examples`

.. _pip: https://pip.pypa.io/en/stable/installing/
