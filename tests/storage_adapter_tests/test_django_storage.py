"""
The test case for the django storage adapter is located in the 'tests'
directory within the Django app example included with this project.
The reason the test case cannot be included with the other storage adapter
tests is because:

1. It needs to be included in the Django app for the 'manage.py test' command
   to run it correctly.
2. The 'examples' directory is not a python module so the 'nosetests' command
   used to run ChatterBot's non-django tests will not detect the Django app
   tests to try to run them.
"""
