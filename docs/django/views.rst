=======================
ChatterBot Django Views
=======================

Example API Views
=================

ChatterBot's Django example comes with an API view that demonstrates
one way to use ChatterBot to create an conversational API endpoint
for your application.

The endpoint expects a JSON request in the following format:

.. code-block:: json

   {"text": "My input statement"}


.. literalinclude:: ../../examples/django_app/example_app/views.py
   :language: python
   :pyobject: ChatterBotApiView


.. note::

   Looking for the full example? Check it out on GitHub:
   https://github.com/gunthercox/ChatterBot/tree/master/examples/django_app
