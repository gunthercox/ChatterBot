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

Using MongoDB with SSL/TLS
--------------------------

For secure connections to remote MongoDB instances (such as Amazon DocumentDB, MongoDB Atlas, or production deployments), you can use SSL/TLS certificates.

Amazon DocumentDB Example
~~~~~~~~~~~~~~~~~~~~~~~~~

Amazon DocumentDB requires SSL/TLS connections with a certificate file. Here's how to configure ChatterBot:

1. Download the Amazon RDS CA certificate bundle:

.. code-block:: bash

   wget https://truststore.pki.rds.amazonaws.com/global/global-bundle.pem

2. Configure ChatterBot to use the certificate:

.. code-block:: python

   from chatterbot import ChatBot

   bot = ChatBot(
       'MyBot',
       storage_adapter='chatterbot.storage.MongoDatabaseAdapter',
       database_uri='mongodb://USERNAME:PASSWORD@my-cluster.us-east-1.docdb.amazonaws.com:27017/?ssl=true&replicaSet=rs0&readPreference=secondaryPreferred',
       mongodb_client_kwargs={
           'tlsCAFile': 'global-bundle.pem'  # Path to your certificate file
       }
   )

MongoDB Atlas Example
~~~~~~~~~~~~~~~~~~~~~

For MongoDB Atlas with SSL/TLS:

.. code-block:: python

   from chatterbot import ChatBot

   bot = ChatBot(
       'MyBot',
       storage_adapter='chatterbot.storage.MongoDatabaseAdapter',
       database_uri='mongodb+srv://USERNAME:PASSWORD@cluster.mongodb.net/?retryWrites=true&w=majority',
       mongodb_client_kwargs={
           'tls': True,
           'tlsAllowInvalidCertificates': False  # Use True only for testing
       }
   )

Self-Signed Certificates
~~~~~~~~~~~~~~~~~~~~~~~~

If you're using self-signed certificates:

.. code-block:: python

   from chatterbot import ChatBot

   bot = ChatBot(
       'MyBot',
       storage_adapter='chatterbot.storage.MongoDatabaseAdapter',
       database_uri='mongodb://localhost:27017/chatterbot-database?ssl=true',
       mongodb_client_kwargs={
           'tlsCAFile': '/path/to/ca.pem',
           'tlsCertificateKeyFile': '/path/to/client.pem',
           'tlsAllowInvalidCertificates': False
       }
   )

Additional MongoDB Client Options
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``mongodb_client_kwargs`` parameter accepts any valid PyMongo MongoClient options, including:

- ``tlsCAFile``: Path to CA certificate file
- ``tlsCertificateKeyFile``: Path to client certificate file
- ``tls``: Enable/disable TLS
- ``tlsAllowInvalidCertificates``: Allow invalid certificates (not recommended for production)
- ``serverSelectionTimeoutMS``: Timeout for server selection
- ``connectTimeoutMS``: Connection timeout
- ``socketTimeoutMS``: Socket timeout
- ``maxPoolSize``: Maximum connection pool size
- ``minPoolSize``: Minimum connection pool size

For a complete list of options, see the `PyMongo MongoClient documentation`_.

MongoDB Adapter Class Attributes
--------------------------------

.. autoclass:: chatterbot.storage.MongoDatabaseAdapter
   :members:

.. _pymongo: https://pypi.org/project/pymongo/
.. _Docker Compose documentation: https://docs.docker.com/compose/
.. _PyMongo MongoClient documentation: https://pymongo.readthedocs.io/en/stable/api/pymongo/mongo_client.html
