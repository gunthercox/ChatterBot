==================
Django integration
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

If you need a ChatterBot API endpont you will want to add the following to your urls.py

.. code-block:: python

   urlpatterns = patterns(
       ...
       url(r'^chatterbot/', include('chatterbot.ext.django_chatterbot.urls', namespace='chatterbot')),
   )


Sync your database
------------------

.. sourcecode:: sh

   python manage.py migrate django_chatterbot

.. note::

   Looking for a working example? Check our the example Django app using
   ChatterBot on GitHub: https://github.com/gunthercox/ChatterBot/tree/master/examples/django_app

.. _Django documentation: https://docs.djangoproject.com/en/dev/intro/install/
