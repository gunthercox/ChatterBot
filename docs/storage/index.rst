================
Storage Adapters
================

Storage adapters provide an interface that allows ChatterBot
to connect to different storage technologies.

.. toctree::
   :maxdepth: 1

   text-search
   create-a-storage-adapter

The storage adapter that your bot uses can be specified by setting
the ``storage_adapter`` parameter to the import path of the
storage adapter you want to use. 

.. code-block:: python

   chatbot = ChatBot(
       "My ChatterBot",
       storage_adapter="chatterbot.storage.SQLStorageAdapter"
   )


Common storage adapter attributes
=================================

Each storage adapter inherits the following attributes and methods.

.. autoclass:: chatterbot.storage.StorageAdapter
   :members:


SQL Storage Adapter
===================

.. autoclass:: chatterbot.storage.SQLStorageAdapter
   :members:

MongoDB Storage Adapter
=======================

.. note::

   Before you can use this storage adapter you will need to install
   `pymongo`_. Consider adding ``pymongo`` to your project's
   ``requirements.txt`` file so you can keep track of your dependencies
   and their versions.

.. autoclass:: chatterbot.storage.MongoDatabaseAdapter
   :members:

Database Migrations
===================

Various frameworks such as Django and SQL Alchemy support
functionality that allows revisions to be made to databases
programmatically. This makes it possible for updates and
revisions to structures in the database to be be applied
in consecutive version releases.

The following explains the included migration process for
each of the databases that ChatterBot comes with support for.

* Django: Full schema migrations and data migrations will
  be included with each release.
* SQL Alchemy: No migrations are currently provided in
  releases. If you require migrations between versions
  `Alembic`_ is the recommended solution for generating them.
* MongoDB: No migrations are provided.

.. _Alembic: https://alembic.sqlalchemy.org
.. _pymongo: https://pypi.org/project/pymongo/
