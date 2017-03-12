===============
Output Adapters
===============

.. toctree::
   :maxdepth: 1

   create-an-output-adapter

Output format adapter
=====================

.. autofunction:: chatterbot.output.OutputAdapter

The output adapter allows the chat bot to return a response in
as a `Statement` object.

.. code-block:: python

   chatbot = ChatBot(
       "My ChatterBot",
       output_adapter="chatterbot.output.OutputAdapter",
       output_format="text"
   )

Terminal output adapter
=======================

.. autofunction:: chatterbot.output.TerminalAdapter

The output terminal adapter allows a user to type into their terminal to
communicate with the chat bot.

.. code-block:: python

   chatbot = ChatBot(
       "My ChatterBot",
       output_adapter="chatterbot.output.TerminalAdapter"
   )

.. _hipchat-output-adapter:

Gitter output adapter
=====================

.. autofunction:: chatterbot.output.Gitter

.. code-block:: python

   chatbot = ChatBot(
       "My ChatterBot",
       output_adapter="chatterbot.output.Gitter",
       gitter_api_token="my-gitter-api-token",
       gitter_room="my-room-name",
       gitter_only_respond_to_mentions=True,
   )

HipChat output adapter
======================

.. autofunction:: chatterbot.output.HipChat

This is an output adapter that allows a ChatterBot instance to send responses
to a `HipChat`_ room.

Be sure to also see the documentation for the :ref:`HipChat input adapter <hipchat-input-adapter>`.

.. code-block:: python

   chatbot = ChatBot(
       "My ChatterBot",
       output_adapter="chatterbot.output.HipChat",
       hipchat_host="https://mydomain.hipchat.com",
       hipchat_room="my-room-name",
       hipchat_access_token="my-hipchat-access-token",
   )

.. _microsoft-output-adapter:

Microsoft Bot Framework output adapter
======================================

.. autofunction:: chatterbot.output.Microsoft

This is an output adapter that allows a ChatterBot instance to send responses
to a `Microsoft`_ using *Direct Line protocol*.

Be sure to also see the documentation for the :ref:`Microsoft input adapter <microsoft-input-adapter>`.

.. code-block:: python

   chatbot = ChatBot(
       "My ChatterBot",
       output_adapter="chatterbot.output.Microsoft",
       direct_line_host="https://directline.botframework.com",
       direct_line_conservationId="IEyJvnDULgn",
       direct_line_token_or_secret="RCurR_XV9ZA.cwA.BKA.iaJrC8xpy8qbOF5xnR2vtCX7CZj0LdjAPGfiCpg4Fv0",
   )

Mailgun output adapter
======================

.. autofunction:: chatterbot.output.Mailgun

The Mailgun adapter allows the chat bot to send emails using the
`Mailgun API`_.

.. literalinclude:: ../../examples/mailgun.py
   :language: python

.. _`Mailgun API`: https://documentation.mailgun.com/api_reference.html
.. _HipChat: https://www.hipchat.com/
.. _Microsoft: https://docs.botframework.com/en-us/restapi/directline/#/Conversations
