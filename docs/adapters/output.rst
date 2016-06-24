===============
Output Adapters
===============

Output format adapter
=====================

.. autofunction:: chatterbot.adapters.output.OutputFormatAdapter

The output format adapter allows the chat bot to return a response in
a number of formats. By default, this adapter returns a :ref:`Statement <conversation_statements>`
object.

Valid parameters for the output format are `text`, `json`, and `object`.

* If `text` is selected, the response will be in string format.
* If `json` is selected, the response will be a dictionary.
* If `object` is selected, the response will be a Statement object.

.. code-block:: python

   chatbot = ChatBot(
       "My ChatterBot",
       output_adapter="chatterbot.adapters.output.OutputFormatAdapter",
       format='text'
   )

Terminal adapter
================

.. autofunction:: chatterbot.adapters.output.TerminalAdapter

The output terminal adapter allows a user to type into their terminal to
communicate with the chat bot.

.. code-block:: python

   chatbot = ChatBot(
       "My ChatterBot",
       output_adapter="chatterbot.adapters.output.TerminalAdapter"
   )

.. _hipchat-output-adapter:

HipChat Adapter
===============

.. autofunction:: chatterbot.adapters.output.HipChat

This is an output adapter that allows a ChatterBot instance to send responses
to a `HipChat`_ room.

Be sure to also see the documentation for the :ref:`HipChat input adapter <hipchat-input-adapter>`.

.. code-block:: python

   chatbot = ChatBot(
       "My ChatterBot",
       input_adapter="chatterbot.adapters.output.HipChat",
       hipchat_host="https://mydomain.hipchat.com",
       hipchat_room="my-room-name",
       hipchat_access_token="my-hipchat-access-token",
   )

Mailgun adapter
===============

.. autofunction:: chatterbot.adapters.output.Mailgun

The Mailgun adapter allows the chat bot to send emails using the
`Mailgun API`_.

.. literalinclude:: ../../examples/mailgun.py
   :language: python

Speech synthesis
================

Check out the `chatterbot-voice`_ package for more information on how to make
your chat bot interact verbally with others.

.. _chatterbot-voice: https://github.com/gunthercox/chatterbot-voice

Creating your own output adapter
================================

.. autofunction:: chatterbot.adapters.output.OutputAdapter

To create your own output adapter you must create a new class that
inherits from the OutputAdapter base class and you must override
the `process_response` method to return a :ref:`Statement <conversation_statements>` object.

Note that you may need to extend the `__init__` method of your custom output
adapter if you intend to save a kwarg parameter that was passed into
the chat bot's constructor.
(An API key might be an example of a parameter you would want to access here.)

.. literalinclude:: ../../chatterbot/adapters/output/output_adapter.py
   :language: python

.. _chatterbot-voice: https://github.com/gunthercox/chatterbot-voice
.. _`Mailgun API`: https://documentation.mailgun.com/api_reference.html
.. _HipChat: https://www.hipchat.com/
