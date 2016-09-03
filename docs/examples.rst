Examples
========

Several simple examples are available to help you get started with ChatterBot.

Terminal Example
----------------

This example program shows how to create a simple terminal client
that allows you to communicate with your chat bot by typing into
your terminal.

.. literalinclude:: ../examples/terminal_example.py
   :language: python

Using MongoDB
-------------

Before you can use ChatterBot's built in adapter for MongoDB,
you will need to `install MongoDB`_. Make sure MongoDB is
running in your environment before you execute your program.
To tell ChatterBot to use this adapter, you will need to set
the `storage_adapter` parameter.

.. code-block:: python

   storage_adapter="chatterbot.adapters.storage.MongoDatabaseAdapter"

.. literalinclude:: ../examples/terminal_mongo_example.py
   :language: python

.. _install MongoDB: https://docs.mongodb.com/manual/installation/
