Redis Vector Storage Adapter
============================

.. note::

   **(March, 2025)**:
   The ``RedisVectorStorageAdapter`` is new and experimental functionality introduced as a "beta" feature. Its functionality might not yet be fully stable and is subject to change in future releases.

.. image:: /_static/Redis_Logo_Red_RGB.svg
   :alt: Redis Logo
   :align: center
   :width: 200
..
    Imaged used in accordance with the Redis Trademark Policy
    https://redis.io/legal/trademark-policy/

The ``RedisVectorStorageAdapter`` allows a ChatterBot instance to store and retrieve text and metadata using a Redis® instance configured as a :term:`vector database`.
This adapter supports the use of vectors when filtering queries to search for similar text.

Vectors are a mathematical representation of text that can be used
to calculate the similarity between two pieces of text based on
the distance between their vectors. This allows for more accurate
search results when looking for similar text because the context of
the text can be taken into account.

For example, consider the following words:

.. code-block:: text

            (Speaking)
                ●
               / \
              /   \
    (Poetry) ●-----● (Rhyming)
              \   /
               \ /
                ●
            (Writing)

The acts of "speaking" and "writing" are both forms of communication, so they are included in the same cluster, but they are somewhat opposite to each other. Both "poetry" and "rhyming" closely related, and in some cases might possibly be used as synonyms within the context of either types of speech or types of writing.

Redis Setup
-----------

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
   :caption: docker-compose.yml

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

   docker compose up -d

Likewise, you can run ``docker compose ps`` to review the status of your container, and ``docker compose down`` to stop it. For more information on Docker and ``docker compose``, see the `Docker Compose documentation`_.

Redis Configuration
-------------------

To use the ``RedisVectorStorageAdapter`` you will need to provide the following argument when configuring your ChatterBot instance:

.. code-block:: python

   from chatterbot import ChatBot

   chatbot = ChatBot(
         'Redis Bot',
         storage_adapter='chatterbot.storage.RedisVectorStorageAdapter,
         # Optional: Override the default Redis URI
         # database_uri='redis://localhost:6379/0'
   )

Class Attributes
----------------

.. autoclass:: chatterbot.storage.RedisVectorStorageAdapter
   :members:

More on Vector Databases
------------------------

For those looking to learn more about vector databases, the following resources can be good starting points:

.. list-table:: Vector Database Learning Resources
   :widths: 50 50
   :header-rows: 1

   * - Article
     - Link
   * - What is a vector database?
     - https://www.mongodb.com/resources/basics/databases/vector-databases
   * - Why use a vector database?
     - https://stackoverflow.blog/2023/09/20/do-you-need-a-specialized-vector-database-to-implement-vector-search-well/
   * - How to choose a vector database?
     - https://learn.microsoft.com/en-us/azure/cosmos-db/mongodb/vcore/vector-search-ai
   * - Redis as a vector database
     - https://redis.io/docs/latest/develop/interact/search-and-query/advanced-concepts/vectors/


:sub:`* Redis is a registered trademark of Redis Ltd. Any rights therein are reserved to Redis Ltd.`


.. _Redis: https://redis.io/docs/latest/operate/oss_and_stack/install/install-redis/
.. _Docker Compose documentation: https://docs.docker.com/compose/
