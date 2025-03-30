MongoDB Storage Adapter
=======================

.. image:: /_static/MongoDB_Fores-Green.svg
   :alt: MongoDB Logo
   :align: center
..
   Imaged used in accordance with the MongoDB Trademark Usage Guidelines
   https://www.mongodb.com/legal/trademark-usage-guidelines

ChatterBot includes support for integration with MongoDB databases via its ``MongoDatabaseAdapter`` class.

Before you can use this storage adapter you will need to install `pymongo`_. An easy way to install it is to use the ``chatterbot[mongodb]`` extra when installing ChatterBot. For example:

.. code-block:: bash

   pip install chatterbot[mongodb]

You'll also need to have a MongoDB server running. An easy way to run one locally is to use Docker:

.. code-block:: yaml
   :caption: docker-compose.yml

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

To start the MongoDB container, run:

.. code-block:: bash

   docker compose up -d

.. note::

   For more information on Docker and ``docker compose``, see the `Docker Compose documentation`_.

MongoDB Adapter Class Attributes
--------------------------------

.. autoclass:: chatterbot.storage.MongoDatabaseAdapter
   :members:

.. _pymongo: https://pypi.org/project/pymongo/
.. _Docker Compose documentation: https://docs.docker.com/compose/
