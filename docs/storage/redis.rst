Redis Vector Storage Adapter
============================

The Redis Vector Storage Adapter allows a ChatterBot instance
to store and retrieve text and metadata using a Redis database.
This adapter supports the use of vectors when filtering queries
to search for similar text.

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

..
   TODO:
     * Links to good resources on vectors
     * Talk about how vectors differ from text search

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

.. _Redis: https://redis.io/docs/latest/operate/oss_and_stack/install/install-redis/
.. _Docker Compose documentation: https://docs.docker.com/compose/
