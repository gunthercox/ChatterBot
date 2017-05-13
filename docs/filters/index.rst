=======
Filters
=======

Filters are an efficient way to create base queries that can be passed to ChatterBot's storage adapters.
Filters will reduce the number of statements that a chat bot has to process when it is selecting a response.

.. toctree::
   :maxdepth: 2

   create_a_new_filter


Setting filters
===============

.. code-block:: python

   chatbot = ChatBot(
       "My ChatterBot",
       filters=["chatterbot.filters.RepetitiveResponseFilter"]
   )

Filter classes
==============

.. autoclass:: chatterbot.filters.RepetitiveResponseFilter
   :members:
