==============================
Django REST Framework Tutorial
==============================

This is the second portion of ChatterBot's Django tutorial. These tutorial are intended to briefly introduce beginners to the basics of Django, Django REST Framework, and other related libraries that provide a powerful foundation of knowledge for developing Python applications. For a more comprehensive tutorial, the `official documentation for Django REST Framework`_ is highly recommended.

In this section, we will be adding a REST API to our Django project from the `previous tutorial <../django-tutorial/index.html>`_.

.. _official documentation for Django REST Framework: https://www.django-rest-framework.org/tutorial/quickstart/


1. Install Django REST Framework
================================

Begin by installing Django REST Framework with the following command:

.. sourcecode:: sh

   pip install djangorestframework

Next, add ``rest_framework`` to your ``INSTALLED_APPS`` in the ``settings.py`` file of your Django project.

.. code-block:: python

   INSTALLED_APPS = (
       # ...
       'rest_framework',
   )

2. Create a Serializer
======================

A serializer is a class that defines the fields that get converted to JSON. Create a new file called ``serializers.py`` in the ``chapters`` directory.

.. code-block:: python

   from rest_framework import serializers
   from chapters.models import Chapter


   class ChapterSerializer(serializers.ModelSerializer):
       class Meta:
           model = Chapter
           fields = (
                'title',
                'number',
           )


3. Create a ViewSet
===================

A viewset is a class that provides the actions that can be performed on a resource. Create a new file called ``viewsets.py`` in the ``chapters`` directory.

.. code-block:: python

   from rest_framework import viewsets
   from chapters.models import Chapter
   from chapters.serializers import ChapterSerializer


   class ChapterViewSet(viewsets.ModelViewSet):
       queryset = Chapter.objects.all()
       serializer_class = ChapterSerializer


4. Add a Router
===============

A router is a class that automatically determines the URL conf for a set of views. You can add your router to your project's existing ``urls.py`` file.

.. code-block:: python

   from django.urls import include
   from rest_framework.routers import DefaultRouter
   from chapters.viewsets import ChapterViewSet

   router = DefaultRouter()
   router.register(r'chapters', ChapterViewSet)

   urlpatterns = [
       # ...
       path('api/', include(router.urls)),
   ]

5. Test Your API
================

To test your API, open a web browser and navigate to ``http://localhost:8000/api/chapters/``. You should see a JSON response with the chapters in your database.

.. code-block:: JSON
    
   [
       {
           "title": "Introduction",
           "number": 1
       }
   ]

6. Conclusion
=============

This concludes this mini tutorial on Django REST Framework. Now you know how to:

- Add a REST API to your Django project
- Create a serializer using Django REST Framework
- Create a viewset and router to expose your API

For further learning, a good place to start would be how to use JavaScript to interact with your API from your webpages.
