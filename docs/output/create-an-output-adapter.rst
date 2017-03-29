Creating a new output adapter
==============================

You can write your own storage adapters by creating a new class that
inherits from :code:`chatterbot.output.OutputAdapter` and overrides the
necessary methods established in the :code:`OutputAdapter` class.

To create your own output adapter you must override the :code:`process_response`
method to return a :ref:`Statement <conversation_statements>` object.

Note that you may need to extend the :code:`__init__` method of your custom output
adapter if you intend to save a kwarg parameter that was passed into
the chat bot's constructor.
(An API key might be an example of a parameter you would want to access here.)

.. literalinclude:: ../../chatterbot/output/output_adapter.py
   :language: python