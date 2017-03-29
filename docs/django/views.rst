=======================
ChatterBot Django Views
=======================

API Views
=========

ChatterBot's django module comes with a pre-built API view that you can make
requests against to communicate with your bot from your web application.

The endpoint expects a JSON request with the following data:

.. code-block:: json

   {"text": "My input statement"}

.. note::

   You will need to include ChatterBot's urls in your django url configuration
   before you can make requests to these views. See the setup instructions for
   more details.
