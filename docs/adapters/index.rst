========
Adapters
========

ChatterBot uses adapter modules to control the behavior of specific types of tasks.
There are four distinct types of adapters that ChatterBot uses,
these are storage adapters, input adapters, output adapters and logic adapters.

.. toctree::
   :maxdepth: 2

   logic
   response_selection
   create-a-logic-adapter
   storage
   create-a-storage-adapter
   input
   create-an-input-adapter
   output
   create-an-output-adapter

Adapters types
--------------

1. Storage adapters - Provide an interface for ChatterBot to connect to various storage systems such as `MongoDB`_ or local file storage.
2. Input adapters - Provide methods that allow ChatterBot to get input from a defined data source.
3. Output adapters - Provide methods that allow ChatterBot to return a response to a defined data source.
4. Logic adapters - Define the logic that ChatterBot uses to respond to input it receives.

Context
-------

When ChatterBot initializes each adapter, it sets an attribute named 'context'. The context variable makes it possible for each adapter to have access to all of the other adapters being used. Perhaps two input and output adapters need to share some information or maybe you want to give your logic adapter direct access to the storage adapter. These are just a few cases where this functionality is useful.

Each adapter can be accessed on the context object from within an adapter by referencing `self.context`. Then, `self.context.storage` refers to the storage adapter, `self.context.input` refers to the input adapter, `self.context.output` refers to the current output adapter, and `self.context.logic` refers to the list of logic adapters.

Adapter defaults
----------------

By default, ChatterBot uses the `JsonFileStorageAdapter` adapter for storage,
the `ClosestMatchAdapter` for logic, the `VariableInputTypeAdapter` for input
and the OutputFormatAdapter for output.

Each adapter can be set by passing in the dot-notated import path to the constructor as shown.

.. code-block:: python

   bot = ChatBot(
       "Elsie",
       storage_adapter="chatterbot.adapters.storage.JsonFileStorageAdapter",
       input_adapter="chatterbot.adapters.input.VariableInputTypeAdapter",
       output_adapter="chatterbot.adapters.output.OutputFormatAdapter",
       logic_adapters=[
           "chatterbot.adapters.logic.ClosestMatchAdapter"
       ],
   )

Third Party Adapters
--------------------

- `chatterbot-voice`_ - A text to speech (tts) and speech recognition adapter designed to use with ChatterBot.
- `chatterbot-weather`_ A ChatterBot logic adapter that returns information about the current weather.

.. _MongoDB: https://docs.mongodb.com/
.. _chatterbot-voice: https://github.com/gunthercox/chatterbot-voice
.. _chatterbot-weather: https://github.com/gunthercox/chatterbot-weather
