Webservices
===========

If you want to host your Django app, you need to choose a method through
which it will be hosted. There are a few free services that you can use
to do this such as `Heroku`_ and `PythonAnyWhere`_.

WSGI
----

A common method for serving Python web applications involves using a
Web Server Gateway Interface (`WSGI`_) package.

`Gunicorn`_ is a great choice for a WSGI server. They have detailed
documentation and installation instructions on their website.

Hosting static files
--------------------

There are numerous ways to host static files for your Django application.
One extreemly easy way to do this is by using `WhiteNoise`_, a python package
designed to make it possible to serve static files from just about any web application.

.. _Heroku: https://dashboard.heroku.com/
.. _PythonAnyWhere: https://www.pythonanywhere.com/details/django_hosting
.. _Gunicorn: http://gunicorn.org/
.. _WhiteNoise: http://whitenoise.evans.io/en/stable/
.. _WSGI: http://wsgi.readthedocs.io/en/latest/what.html
