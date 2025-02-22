========================
Django Tutorial (Part 2)
========================

In the :ref:`previous part <Django Tutorial (Part 1)>` of this tutorial we set up our Django app. Now we're going to create a new model, and a view. If this is your first time working with these, Django's models are classes that represent database tables, and Django's views are functions that handle HTTP requests and return  HTTP responses.

1. Creating a New Model
=======================

In the ``chapters`` directory, open the file ``models.py``. This file is where you define your models. Add the following code to the file:

.. code-block:: python
    :caption: chapters/models.py

    from django.db import models


    class Chapter(models.Model):
        """
        A model representing a chapter in a digital book.
        """
        title = models.CharField(max_length=100)
        number = models.IntegerField(unique=True)

Next, run the following commands. The first will generate a migration file, code that tells Django how to create a new table in a database to correspond to this model. The second will run the migration, and create the table in the database.

.. sourcecode:: sh

    python manage.py makemigrations
    python manage.py migrate

You should see output similar to the following:

.. code-block:: sh

    Migrations for 'chapters':
      chapters/migrations/0001_initial.py
        - Create model Chapter

    Operations to perform:
      Apply all migrations: admin, auth, chapters, contenttypes, sessions
    Running migrations:
      Applying contenttypes.0001_initial... OK
      Applying auth.0001_initial... OK
      Applying admin.0001_initial... OK
      Applying admin.0002_logentry_remove_auto_add... OK
      Applying admin.0003_logentry_add_action_flag_choices... OK
      Applying contenttypes.0002_remove_content_type_name... OK
      Applying auth.0002_alter_permission_name_max_length... OK
      Applying auth.0003_alter_user_email_max_length... OK
      Applying auth.0004_alter_user_username_opts... OK
      Applying auth.0005_alter_user_last_login_null... OK
      Applying auth.0006_require_contenttypes_0002... OK
      Applying auth.0007_alter_validators_add_error_messages... OK
      Applying auth.0008_alter_user_username_max_length... OK
      Applying auth.0009_alter_user_last_name_max_length... OK
      Applying auth.0010_alter_group_name_max_length... OK
      Applying auth.0011_update_proxy_permissions... OK
      Applying auth.0012_alter_user_first_name_max_length... OK
      Applying chapters.0001_initial... OK
      Applying sessions.0001_initial... OK


2. Creating a New View
======================

In Django, views let you define what content gets returned in response to a request. In this part of the tutorial, we're going to set up a view that renders an HTML page for the requested chapter and populate that page with the corresponding data using the model we previously created.

Start by creating a new file and folder in the ``chapters`` directory: ``templates/chapter.html``. Add the following code to the file:

.. code-block:: html
    :caption: chapters/templates/chapter.html

    <!DOCTYPE html>
    <html>
    <head>
        <title>{{ chapter.title }}</title>
    </head>
    <body>
        <h1>{{ chapter.title }}</h1>
        <p>This is chapter {{ chapter.number }}.</p>
    </body>
    </html>

In the ``chapters`` directory, open the file ``chapters/views.py``. This file is where you define your views. Add the following code to the file:

.. code-block:: python
    :caption: chapters/views.py

    from django.views.generic import TemplateView
    from django.http import HttpResponse
    from chapters.models import Chapter

    class ChapterView(TemplateView):
        """
        Render an HTML page for the requested chapter.
        """

        template_name = 'chapter.html'

        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)

            context['chapter'] = Chapter.objects.get(number=kwargs['number'])

            return context


Finally, open the file ``tutorial/urls.py``. This file is where you define the URLs for your views. Ensure the following import for ``ChapterView`` is at the top of the file, and that the ``path`` for the view is included in the ``urlpatterns`` list:

.. code-block:: python
    :caption: tutorial/urls.py

    from django.urls import path
    from chapters.views import ChapterView

    urlpatterns = [
        path('chapter/<int:number>/', ChapterView.as_view(), name='chapter'),
    ]


3. Adding a Chapter
===================

To add a chapter to the database, run the following command:

.. sourcecode:: sh

    python manage.py shell


This will open a Python shell. Run the following commands to create a new chapter:

.. code-block:: python

    from chapters.models import Chapter

    Chapter.objects.create(title='Introduction', number=1)


Use ``Ctrl-D`` or type in ``exit()`` to exit the shell.

Now you should be able to visit ``http://localhost:8000/chapter/1/`` in your web browser and see the chapter page you created.

4. Concluding Part 2
====================

This concludes part 2 of this mini Django tutorial. Now you know:

- How to create a new model in Django
- How to generate and run migrations
- How to add views with html templates
- How to add a url for your views
- How to add data to your database using Django's shell

If you still want to learn more, `Django's official documentation <https://docs.djangoproject.com/en/4.2/contents/>`_ is a great place to start. 

:ref:`Up next <Django REST Framework Tutorial>` in this series we'll be building off of the project we've begun to learn about how to add Django REST Framework to an existing Django project.
