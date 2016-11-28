========
Sessions
========

ChatterBot supports the ability to have multiple concurrent chat sessions.
A chat session is where the chat bot interacts with a person, and supporting
multiple chat sessions means that your chat bot can have multiple different
conversations with different people at the same time.

.. autoclass:: chatterbot.conversation.session.Session
   :members:

.. autoclass:: chatterbot.conversation.session.SessionManager
   :members:

Each session object holds a queue of the most recent communications that have
occured durring that session. The queue holds tuples with two values each,
the first value is the input that the bot recieved and the second value is the
response that the bot returned.

.. autoclass:: chatterbot.queues.ResponseQueue
   :members: