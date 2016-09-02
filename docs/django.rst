============================
Using ChatterBot with Django
============================

ChatterBot has direct support for integration with Django. ChatterBot provides
out of the box models and endpoints that allow you build ChatterBot powered
Django applications.

Installation
============

Install with pip

    pip install django chatterbot

For more details on installing Django, see the `Django documentation`_.


Add `chatterbot.ext.django_chatterbot` to your `INSTALLED_APPS`

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'chatterbot.ext.django_chatterbot',,
    )


If you need a ChatterBot API endpont you will want to add the following to your urls.py

.. code-block:: python

    urlpatterns = patterns(
        ...
        url(r'^chatterbot/', include('chatterbot.ext.django_chatterbot.urls', namespace='chatterbot')),
    )

Sync your database
------------------

.. sourcecode:: sh

    $ python manage.py migrate chatterbot.ext.django_chatterbot

.. _Django documentation: https://docs.djangoproject.com/en/dev/intro/install/
