==================
Django Integration
==================

ChatterBot has direct support for integration with Django. ChatterBot provides
out of the box models and endpoints that allow you build ChatterBot powered
Django applications.

.. toctree::
   :maxdepth: 2

   settings
   training
   views
   wsgi

Install packages
================

Install with pip

.. sourcecode:: sh

   pip install django chatterbot

For more details on installing Django, see the `Django documentation`_.

Installed Apps
--------------

Add `chatterbot.ext.django_chatterbot` to your `INSTALLED_APPS`

.. code-block:: python

   INSTALLED_APPS = (
       # ...
       'chatterbot.ext.django_chatterbot',
   )


API view
--------

If you need a ChatterBot API endpoint you will want to add the following to your urls.py

.. code-block:: python

   urlpatterns = patterns(
       ...
       url(r'^chatterbot/', include('chatterbot.ext.django_chatterbot.urls', namespace='chatterbot')),
   )


Migrations
----------

.. sourcecode:: sh

   python manage.py migrate django_chatterbot

.. note::

   Looking for a working example? Check our the example Django app using
   ChatterBot on GitHub: https://github.com/gunthercox/ChatterBot/tree/master/examples/django_app

MongoDB and Django
------------------

ChatterBot has a storage adapter for MongoDB but it does not work with Django.
If you want to use MongoDB as your database for Django and your chat bot then
you will need to install a **Django storage backend** such as `Django MongoDB Engine`_.

The reason this is required is because Django's storage backends are different
and completely separate from ChatterBot's storage adapters.

.. _Django documentation: https://docs.djangoproject.com/en/dev/intro/install/
.. _Django MongoDB Engine: https://django-mongodb-engine.readthedocs.io/
