======================
django-filter tutorial
======================

In this section, we will be adding filtering functionality to the API built in the :ref:`Django REST Framework Tutorial`. To do this we'll be using the `django-filter` package.

For more information, ``django-filter`` has a comprehensive setup guide in its `documentation <https://django-filter.readthedocs.io/en/stable/guide/rest_framework.html>`_.

1. Install django-filter
========================

To install ``django-filter``, run the following command:

.. sourcecode:: sh

   pip install django-filter


2. Configure django-filter settings
===================================

Add ``django_filters`` to your ``INSTALLED_APPS`` in the ``settings.py`` file of your Django project.

.. code-block:: python

   INSTALLED_APPS = (
       # ...
       'django_filters',
   )

Also add the following lines to the ``REST_FRAMEWORK`` setting in the same file:

.. code-block:: python

   REST_FRAMEWORK = {
       'DEFAULT_FILTER_BACKENDS': (
           'django_filters.rest_framework.DjangoFilterBackend',
           # ...
       )
   }


3. Configure filtering for the API
==================================

Define a new ``filterset_fields`` variable at the class level of the viewset you created in the previous tutorial:

.. code-block:: python

    # ...

    class ChapterViewSet(viewsets.ModelViewSet):
        queryset = Chapter.objects.all()
        serializer_class = ChapterSerializer

        # Add this line:
        filterset_fields = ('number', 'title')

    # ...

4. Test the filtering
=====================

You can now test the filtering by adding query parameters to the API URL. For example, to filter chapters by title, you can use the following URL:

.. code-block:: text

   http://localhost:8000/api/chapters?title=Introduction&number=1


You'll see that only the chapter with the title "Introduction" and number "1" is returned in the response. Note that you may need to add more chapters to your database to fully see the filtering in action.

5. Conclusion on django-filter
==============================

Now you know how to add filtering functionality to your APIs. The ``django-filter`` package has a number of additional features including the ability to create more complex and custom filters. For more information, see the `django-filter documentation <https://django-filter.readthedocs.io/en/stable/guide/rest_framework.html>`_.

To wrap up these tutorials, in the :ref:`next section <Writing Tests for Django Applications>` we'll be covering how to write tests for the API you just built.
