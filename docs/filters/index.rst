=======
Filters
=======

Filters are an efficient way to create base queries that can be passed to ChatterBot's storage adapters.

.. toctree::
   :maxdepth: 2

   create_a_new_filter

Repetitive response filter
==========================

.. autofunction:: chatterbot.filters.RepetitiveResponseFilter

.. code-block:: python

   chatbot = ChatBot(
       "My ChatterBot",
       filters="chatterbot.filters.RepetitiveResponseFilter"
   )

