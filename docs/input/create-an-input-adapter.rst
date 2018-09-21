Creating a new input adapter
==============================

You can write your own input adapters by creating a new class that
inherits from ``InputAdapter`` and overrides the necessary
methods established in the base ``InputAdapter`` class.

.. autofunction:: chatterbot.input.InputAdapter

To create your own input adapter you must override the ``process_input``
method to return a :ref:`Statement <conversation_statements>` object.

Note that you may need to extend the ``__init__`` method of your custom input
adapter if you intend to save a kwarg parameter that was passed into
the chat bot's constructor.
(An API key might be an example of a parameter you would want to access here.)

.. literalinclude:: ../../chatterbot/input/input_adapter.py
   :language: python
