=================
Django ChatterBot
=================

This is a Django project that makes it possible to create a simple chat bot web
app using Django_, `Django REST framework`_ and ChatterBot_.

Installation
------------

   pip install django chatterbot

Quick start
-----------

1. Add ChatterBot's Django app module to your INSTALLED_APPS setting like this:

   INSTALLED_APPS = (
       ...
       'chatterbot.ext.django_chatterbot',
   )

2. Include the URLconf in your project urls.py like this:
   from chatterbot.ext.django_chatterbot import urls as chatterbot_urls

   urlpatterns = [
       ...
       url(r'^api/chatterbot/', include(chatterbot_urls, namespace='chatterbot')),
   ]

3. Run `python manage.py migrate` to create the chatterbot models.

4. Start your Django app `python manage.py runserver 0.0.0.0:8000`

5. POST to http://127.0.0.1:8000/api/chatterbot/ to start a conversation.

   {'text': 'Hello, how are you?'}

.. _Django: https://www.djangoproject.com
.. _Django REST framework: http://www.django-rest-framework.org
.. _ChatterBot: https://github.com/gunthercox/ChatterBot
