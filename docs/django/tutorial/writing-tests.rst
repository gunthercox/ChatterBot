=====================================
Writing Tests for Django Applications
=====================================

Writing tests helps ensure the quality and stability of your code. Creating tests from the start of a project is often easier than adding them later, and writing good tests can help establish beneficial patterns that others can copy later when adding new features.

This tutorial will show you how to write tests for Django applications, specifically for Django REST framework APIs.

Example API Test Cases
=======================

Here are a few examples of test cases for the API that we built as a part of the :ref:`previous tutorials <Django Tutorials>`.

A few things to note:

- We use Django's ``reverse`` function to generate the URL for the API endpoint. This helps ensure that the tests will continue to work even if the URL changes.
- We use Django REST framework's ``APITestCase`` class to write the test cases. This is preferred for API tests over Django's built-in ``TestCase`` classes because it provides additional features that are useful for testing APIs.
- The ``status`` module from Django REST framework is used to check the status codes of the responses. Although not necessary, it helps keep tests more readable.

.. code-block:: python

    from django.urls import reverse
    from rest_framework import status
    from rest_framework.test import APITestCase
    from chapters.models import Chapter


    class ChapterListApiTests(APITestCase):
        """
        Test cases for the /chapter/ endpoint.
        """

        def setUp(self):
            # Use Django's reverse function to generate the URL
            self.endpoint = reverse('chapter-list')

        def test_list_chapters(self):
            """
            A list of chapters should be returned from the API.
            """
            # Create a chapter
            Chapter.objects.create(title='Introduction', number=1)

            response = self.client.get(self.endpoint, format='json')

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data, {
                'count': 1,
                'next': None,
                'previous': None,
                'results': [
                    {'title': 'Introduction', 'number': 1}
                ]
            })

        def test_filter_chapters_by_number(self):
            """
            The matching chapters should be returned from the API when filtering by number.
            """
            # Create chapters
            Chapter.objects.create(title='Introduction', number=1)
            Chapter.objects.create(title='Prologue', number=2)

            response = self.client.get(self.endpoint + '?number=1', format='json')

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data, {
                'count': 1,
                'next': None,
                'previous': None,
                'results': [
                    {'title': 'Introduction', 'number': 1}
                ]
            })

        def test_create_chapter(self):
            """
            A chapter should be created when a POST request is sent to the API.
            """
            response = self.client.post(self.endpoint, {
                'title': 'Introduction', 'number': 1
            }, format='json')

            # Only one chapter should exist
            self.assertEqual(Chapter.objects.count(), 1)

            chapter = Chapter.objects.first()

            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(chapter.title, 'Introduction')
            self.assertEqual(chapter.number, 1)


    class ChapterDetailApiTests(APITestCase):
        """
        Test cases for the /chapter/<id>/ endpoint.
        """

        def setUp(self):
            self.chapter = Chapter.objects.create(title='Introduction', number=1)
            self.endpoint = reverse('chapter-detail', args=[self.chapter.id])

        def test_update_chapter(self):
            """
            A chapter should be updated when a PATCH request is sent to the API.
            """

            response = self.client.patch(reverse('chapter-detail', args=[self.chapter.id]), {
                'title': 'Introduction', 'number': 2
            }, format='json')

            # Only one chapter should exist
            self.assertEqual(Chapter.objects.count(), 1)

            chapter = Chapter.objects.first()

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(chapter.number, 2)

        def test_delete_chapter(self):
            """
            A chapter should be deleted when a DELETE request is sent to the API.
            """
            response = self.client.delete(reverse('chapter-detail', args=[self.chapter.id]))

            # No chapters should exist
            self.assertEqual(Chapter.objects.count(), 0)
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
