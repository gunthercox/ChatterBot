======================
Python String Encoding
======================

The Python developer community has published a great article that covers the
details of unicode character processing.

- Python 3: https://docs.python.org/3/howto/unicode.html
- Python 2: https://docs.python.org/2/howto/unicode.html

The following notes are intended to help answer some common questions and issues
that developers frequently encounter while learning to properly work with different 
character encodings in Python.

Does ChatterBot handle non-ascii characters?
============================================

ChatterBot is able to handle unicode values correctly. You can pass to it
non-encoded data and it should be able to process it properly
(you will need to make sure that you decode the output that is returned).

Below is one of ChatterBot's tests from `tests/test_chatbot.py`_,
this is just a simple check that a unicode response can be processed.

.. code-block:: python

   def test_get_response_unicode(self):
       """
       Test the case that a unicode string is passed in.
       """
       response = self.chatbot.get_response(u'سلام')
       self.assertGreater(len(response.text), 0)

This test passes Python 3. It also verifies that
ChatterBot *can* take unicode input without issue.

How do I fix Python encoding errors?
====================================

When working with string type data in Python, it is possible to encounter errors
such as the following.

.. code-block:: text

   UnicodeDecodeError: 'utf8' codec can't decode byte 0x92 in position 48: invalid start byte

Depending on what your code looks like, there are a few things that you can do
to prevent errors like this.

Unicode header
--------------

.. code-block:: python

   # -*- coding: utf-8 -*-

When to use the unicode header
++++++++++++++++++++++++++++++

If your strings use escaped unicode characters (they look like ``u'\u00b0C'``) then
you do not need to add the header. If you use strings like ``'ØÆÅ'`` then you are required
to use the header.

If you are using this header it must be the first line in your Python file.

Unicode escape characters
-------------------------

.. code-block:: text

   >>> print u'\u0420\u043e\u0441\u0441\u0438\u044f'
   Россия

When to use escape characters
+++++++++++++++++++++++++++++

Prefix your strings with the unicode escape character ``u'...'`` when you are
using escaped unicode characters.

Import unicode literals from future
-----------------------------------

.. code-block:: python

   from __future__ import unicode_literals

When to import unicode literals
+++++++++++++++++++++++++++++++

Use this when you need to make sure that Python 3 code also works in Python 2.

A good article on this can be found here: http://python-future.org/unicode_literals.html

.. _`tests/test_chatbot.py`: https://github.com/gunthercox/ChatterBot/blob/master/tests/test_chatbot.py
