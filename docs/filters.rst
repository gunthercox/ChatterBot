=======
Filters
=======

Filters are an efficient way to create queries that can be passed to ChatterBot's storage adapters.
Filters will reduce the number of statements that a chat bot has to process when it is selecting a response.

Setting filters
===============

.. code-block:: python

   chatbot = ChatBot(
       "My ChatterBot",
       filters=[filters.get_recent_repeated_responses]
   )

.. automodule:: chatterbot.filters
   :members:
