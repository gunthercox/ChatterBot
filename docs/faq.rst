==========================
Frequently Asked Questions
==========================

This document is comprised of questions that are frequently
asked about ChatterBot and chat bots in general.

.. toctree::
   :maxdepth: 2

   encoding

How do I deploy my chat bot to the web?
---------------------------------------

There are a number of excellent web frameworks for creating
Python projects out there. Django and Flask are two excellent
examples of these. ChatterBot is designed to be agnostic to
the platform it is deployed on and it is very easy to get set up.

To run ChatterBot inside of a web application you just need a way
for your application to receive incoming data and to return data.
You can do this any way you want, HTTP requests, web sockets, etc.

There are a number of existing examples that show how to do this.

1. An example using Django: https://github.com/gunthercox/ChatterBot/tree/master/examples/django_app
2. An example using Flask: https://github.com/chamkank/flask-chatterbot/blob/master/app.py