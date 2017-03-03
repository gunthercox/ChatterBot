========
Sessions
========

ChatterBot supports the ability to have multiple concurrent chat sessions.
A chat session is where the chat bot interacts with a person, and supporting
multiple chat sessions means that your chat bot can have multiple different
conversations with different people at the same time.

.. autoclass:: chatterbot.conversation.session.Session
   :members:

.. autoclass:: chatterbot.conversation.session.ConversationSessionManager
   :members:

Each session object holds a queue of the most recent communications that have
occured durring that session. The queue holds tuples with two values each,
the first value is the input that the bot recieved and the second value is the
response that the bot returned.

.. autoclass:: chatterbot.queues.ResponseQueue
   :members:

Session scope
-------------

If two :code:`ChatBot` instances are created, each will have sessions separate from each other.

An adapter can access any session as long as the unique identifier for the session is provided.

Session example 
---------------

The following example is taken from the Django :code:`ChatterBotView` built into ChatterBot.
In this method, the unique identifiers for each chat session are being stored in Django's
session objects. This allows different users who interact with the bot through different
web browsers to have seperate conversations with the chat bot.

.. literalinclude:: ../chatterbot/ext/django_chatterbot/views.py
   :language: python
   :pyobject: ChatterBotView.post
   :dedent: 4
