Creating a new input adapter
==============================

You can write your own storage adapters by creating a new class that
inherits from :code:`InputAdapter` and overides the overrides necessary
methods established in the base :code:`InputAdapter` class.

.. autofunction:: chatterbot.input.InputAdapter

To create your own input adapter you must override the :code:`process_input`
method to return a :ref:`Statement <conversation_statements>` object.

Note that you may need to extend the :code:`__init__` method of your custom input
adapter if you intend to save a kwarg parameter that was passed into
the chat bot's constructor.
(An API key might be an example of a parameter you would want to access here.)

.. literalinclude:: ../../chatterbot/adapters/input/input_adapter.py
   :language: python