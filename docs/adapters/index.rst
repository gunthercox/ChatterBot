Adapters
========

ChatterBot uses adapter modules to control the behavior of specific types of tasks.
There are four distinct types of adapters that ChatterBot uses,
these are storage adapters, input adapters, output adapters and logic adapters.

.. toctree::
   :maxdepth: 2

   storage
   logic
   input
   output

Adapters types
--------------

1. Storage adapters - Provide an interface for ChatterBot to connect to various storage systems such as `MongoDB`_ or local file storage.
2. Input adapters - Provide methods that allow ChatterBot to get input from a defined data source.
3. Output adapters - Provide methods that allow ChatterBot to return a response to a defined data source.
4. Logic adapters - Define the logic that ChatterBot uses to respond to input it receives.

Adapter defaults
----------------

By default, ChatterBot uses the `JsonDatabaseAdapter` adapter for storage,
the `ClosestMatchAdapter` for logic, and the `TerminalAdapter` for input and output.

Each adapter can be set by passing in the dot-notated import path to the constructor as shown.

.. code-block:: python

   bot = ChatBot(
       "Elsie",
       storage_adapter="chatterbot.adapters.storage.JsonDatabaseAdapter",
       input_adapter="chatterbot.adapters.input.TerminalAdapter",
       output_adapter="chatterbot.adapters.output.TerminalAdapter",
       logic_adapters=[
           "chatterbot.adapters.logic.ClosestMatchAdapter"
       ],
   )

.. _MongoDB: https://docs.mongodb.com/
