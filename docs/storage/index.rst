================
Storage Adapters
================

Storage adapters provide an interface that allows ChatterBot
to connect to different storage technologies.

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


Redis Vector Storage Adapter
============================

The Redis Vector Storage Adapter allows a ChatterBot instance
to store and retrieve text and metadata using a Redis database.
This adapter supports the use of vectors when filtering queries
to search for similar text.

..
   TODO:
     * Include diagram of vectors
     * Talk about how vectors differ from text search

**Redis Setup**

Before you use the ``RedisVectorStorageAdapter`` you will need to install
the dependencies required for `Redis`_ and generating vectors.
This can be done using the ``chatterbot[redis]`` extra when
installing ChatterBot. For example:

.. code-block:: bash

   pip install chatterbot[redis]

You will also need to have a Redis server running, with the additional
modules installed that enable searching using vectors. And easy way to
run one locally is to use Docker:

.. code-block:: yaml

   version: "3.8"

   services:
     redis:
       # Use the latest version of the redis-stack image
       image: redis/redis-stack-server:latest
       # Expose the default Redis port
       ports:
         - "6379:6379"
       # Persist the Redis data
       volumes:
         - ./.database/redis/:/data

To start the Redis container, run:

.. code-block:: bash

   docker-compose up -d

.. note::

   For more information on Docker and ``docker-compose``, see the `Docker Compose documentation`_.

**Class Attributes**

.. autoclass:: chatterbot.storage.RedisVectorStorageAdapter
   :members:


SQL Storage Adapter
===================

.. autoclass:: chatterbot.storage.SQLStorageAdapter
   :members:

MongoDB Storage Adapter
=======================

Before you can use this storage adapter you will need to install `pymongo`_. An easy way to install it is to use the ``chatterbot[mongodb]`` extra when installing ChatterBot. For example:

.. code-block:: bash

   pip install chatterbot[mongodb]

You'll also need to have a MongoDB server running. An easy way to run one locally is to use Docker:

.. code-block:: yaml

   version: "3.8"

   services:
     mongo:
       # Use the latest stable version of the mongo image
       image: mongo:8.0
       # Expose the default MongoDB port
       ports:
         - "27017:27017"
       # Persist the MongoDB data
       volumes:
         - ./.database/mongodb/db:/data/db

To start the Redis container, run:

.. code-block:: bash

   docker-compose up -d

.. note::

   For more information on Docker and ``docker-compose``, see the `Docker Compose documentation`_.

**Class Attributes**

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

Further Reading
===============

.. toctree::
   :maxdepth: 1

   text-search
   create-a-storage-adapter

.. _Alembic: https://alembic.sqlalchemy.org
.. _pymongo: https://pypi.org/project/pymongo/
.. _Redis: https://redis.io/docs/latest/operate/oss_and_stack/install/install-redis/
.. _Docker Compose documentation: https://docs.docker.com/compose/
