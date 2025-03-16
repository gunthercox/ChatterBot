=========================
ChatterBot Django Example
=========================

This is an example Django app that shows how to create a simple chat bot web
app using Django_ and ChatterBot_.

Quick Start
-----------

To run this example you will need to have Django and ChatterBot installed. The `requirements.txt` file contains the recommended versions of these packages for this example project.

```bash
pip install -r requirements.txt
```

Run the Django migrations to populate ChatterBot database tables:

```bash
python manage.py migrate
```

Start the Django app by running the following:

```bash
python manage.py runserver 0.0.0.0:8000
```

Documentation
-------------

Further documentation on getting set up with Django and ChatterBot can be
found in the `ChatterBot documentation`_.

.. _Django: https://www.djangoproject.com
.. _ChatterBot: https://github.com/gunthercox/ChatterBot
.. _ChatterBot documentation: https://docs.chatterbot.us/django/
