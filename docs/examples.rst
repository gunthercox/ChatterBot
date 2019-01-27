========
Examples
========

The following examples are available to help you get started with ChatterBot.

.. note::
   Before you run any example, you will need to install ChatterBot on your system.
   See the :ref:`Setup guide <Installation>` for instructions.

Simple Example
==============

.. literalinclude:: ../examples/basic_example.py
   :language: python

Terminal Example
================

This example program shows how to create a simple terminal client
that allows you to communicate with your chat bot by typing into
your terminal.

.. literalinclude:: ../examples/terminal_example.py
   :language: python

Using MongoDB
=============

Before you can use ChatterBot's built in adapter for MongoDB,
you will need to `install MongoDB`_. Make sure MongoDB is
running in your environment before you execute your program.
To tell ChatterBot to use this adapter, you will need to set
the `storage_adapter` parameter.

.. code-block:: python

   storage_adapter="chatterbot.storage.MongoDatabaseAdapter"

.. literalinclude:: ../examples/terminal_mongo_example.py
   :language: python

Time and Mathematics Example
============================

ChatterBot has natural language evaluation capabilities that
allow it to process and evaluate mathematical and time-based
inputs.

.. literalinclude:: ../examples/math_and_time.py
   :language: python

Using SQL Adapter
=================

ChatterBot data can be saved and retrieved from SQL databases.

.. literalinclude:: ../examples/memory_sql_example.py
   :language: python

Read only mode
==============

Your chat bot will learn based on each new input statement it receives.
If you want to disable this learning feature after your bot has been trained,
you can set `read_only=True` as a parameter when initializing the bot.

.. code-block:: python

   chatbot = ChatBot("Johnny Five", read_only=True)

More Examples
=============

Even more examples can be found in the ``examples`` directory on GitHub:
https://github.com/gunthercox/ChatterBot/tree/master/examples 

.. _install MongoDB: https://docs.mongodb.com/manual/installation/
