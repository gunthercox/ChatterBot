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

Gitter Adapter
==============

.. autofunction:: chatterbot.adapters.input.Gitter

.. code-block:: python

   chatbot = ChatBot(
       "My ChatterBot",
       input_adapter="chatterbot.adapters.input.Gitter",
       gitter_api_token="my-gitter-api-token",
       gitter_room="my-room-name",
       gitter_only_respond_to_mentions=True,
   )


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

Mailgun adapter
===============

.. autofunction:: chatterbot.adapters.input.Mailgun

The Mailgun adapter allows a chat bot to recieve emails using
the `Mailgun API`_.

.. literalinclude:: ../../examples/mailgun.py
   :language: python

MicrosotBot Adapter
===================

.. autofunction:: chatterbot.adapters.input.Microsoft

This is an input adapter that allows a ChatterBot instance to communicate
through `Microsoft`_ using *direct line client* protocol.

Be sure to also see the documentation for the :ref:`Microsoft output adapter <microsoft-output-adapter>`.

.. code-block:: python

   chatbot = ChatBot(
       "My ChatterBot",
       input_adapter="chatterbot.adapters.input.Microsoft",
       directline_host="https://directline.botframework.com",
       dirctline_conversation_id="IEyJvnDULgn",
       directline_access_token_or_secret="RCurR_XV9ZA.cwA.BKA.iaJrC8xpy8qbOF5xnR2vtCX7CZj0LdjAPGfiCpg4Fv0",
   )

Speech recognition
==================

Check out the `chatterbot-voice`_ package for more information on how to make
your chat bot interact verbally with others.

.. _strings: https://docs.python.org/2/library/string.html
.. _dictionaries: https://docs.python.org/2/tutorial/datastructures.html#dictionaries
.. _chatterbot-voice: https://github.com/gunthercox/chatterbot-voice
.. _HipChat: https://www.hipchat.com/
.. _`Mailgun API`: https://documentation.mailgun.com/api_reference.html
.. _Microsoft: https://docs.botframework.com/en-us/restapi/directline/#/Conversations
