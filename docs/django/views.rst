=======================
ChatterBot Django Views
=======================

.. note::

   Looking for the full example app? Check it out on GitHub:
   https://github.com/gunthercox/ChatterBot/tree/master/examples/django_example

Example API Views
=================

ChatterBot's Django example comes with an API view that demonstrates
one way to use ChatterBot to create an conversational API endpoint
for your application.

The endpoint expects a JSON request in the following format:

.. code-block:: json

   {"text": "My input statement"}


.. literalinclude:: ../../examples/django_example/django_example/views.py
   :language: python
   :pyobject: ChatterBotApiView
