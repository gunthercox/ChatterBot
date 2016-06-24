==============
Input Adapters
==============

ChatterBot's input adapters are designed to allow a chat bot to have a
versatile method of receiving or retrieving input from a given source.

The goal of a input adapter is to get input from some source, and then
to convert it into a format that ChatterBot can understand. This format
is the :ref:`Statement <conversation_statements>` object found in ChatterBot's
`conversation` module.

Variable input type adapter
===========================

.. autofunction:: chatterbot.adapters.input.VariableInputTypeAdapter

The variable input type adapter allows the chat bot to accept a number
of different input types using the same adapter. This adapter accepts
strings_, dictionaries_ and :ref:`Statements <conversation_statements>`.

.. code-block:: python

   chatbot = ChatBot(
       "My ChatterBot",
       input_adapter="chatterbot.adapters.input.VariableInputTypeAdapter"
   )

Terminal adapter
================

.. autofunction:: chatterbot.adapters.input.TerminalAdapter

The input terminal adapter allows a user to type into their terminal to
communicate with the chat bot.

.. code-block:: python

   chatbot = ChatBot(
       "My ChatterBot",
       input_adapter="chatterbot.adapters.input.TerminalAdapter"
   )

.. _hipchat-input-adapter:

HipChat Adapter
===============

.. autofunction:: chatterbot.adapters.input.HipChat

This is an input adapter that allows a ChatterBot instance to communicate
through `HipChat`_.

Be sure to also see the documentation for the :ref:`HipChat output adapter <hipchat-output-adapter>`.

.. code-block:: python

   chatbot = ChatBot(
       "My ChatterBot",
       input_adapter="chatterbot.adapters.input.HipChat",
       hipchat_host="https://mydomain.hipchat.com",
       hipchat_room="my-room-name",
       hipchat_access_token="my-hipchat-access-token",
   )

Speech recognition
==================

Check out the `chatterbot-voice`_ package for more information on how to make
your chat bot interact verbally with others.

Creating your own input adapter
===============================

.. autofunction:: chatterbot.adapters.input.InputAdapter

To create your own input adapter you must create a new class that
inherits from the InputAdapter base class and you must override
the `process_input` method to return a :ref:`Statement <conversation_statements>` object.

Note that you may need to extend the `__init__` method of your custom input
adapter if you intend to save a kwarg parameter that was passed into
the chat bot's constructor.
(An API key might be an example of a parameter you would want to access here.)

.. literalinclude:: ../../chatterbot/adapters/input/input_adapter.py
   :language: python

.. _strings: https://docs.python.org/2/library/string.html
.. _dictionaries: https://docs.python.org/2/tutorial/datastructures.html#dictionaries
.. _chatterbot-voice: https://github.com/gunthercox/chatterbot-voice
.. _HipChat: https://www.hipchat.com/
