==================================
Packaging your code for ChatterBot
==================================

There are cases where developers may want to contribute code to ChatterBot but for
various reasons it doesn't make sense or isn't possible to add the code to the
main ChatterBot repository on GitHub.

Common reasons that code can't be contributed include:

- Licencing: It may not be possible to contribute code to ChatterBot due to a licencing restriction or a copyright.
- Demand: There needs to be a general demand from the open source community for a particular feature so that there are developers who will want to fix and improve the feature if it requires maintenance.

In addition, all code should be well documented and thoroughly tested.

Package directory structure
---------------------------

Suppose we want to create a new logic adapter for ChatterBot and add it the
Python Package Index (PyPI) so that other developers can install it and use it.
We would begin doing this by setting up a directory file the following structure.

.. literalinclude:: _includes/python_module_structure.txt
   :caption: Python Module Structure

More information on creating Python packages can be found here:
https://packaging.python.org/tutorials/distributing-packages/

Register on PyPI
================

Create an account: https://pypi.python.org/pypi?%3Aaction=register_form

Create a ``.pypirc`` configuration file.

.. code-block:: bash
   :caption: .pypirc file contents

   [distutils]
   index-servers =
   pypi

   [pypi]
   username=my_username
   password=my_password

Generate packages
=================

.. code-block:: bash

   python setup.py sdist bdist_wheel

Upload packages
===============

The official tool for uploading Python packages is called twine.
You can install twine with pip if you don't already have it installed.

.. code-block:: bash

   pip install twine

.. code-block:: bash

   twine upload dist/*

Install your package locally
============================

.. code-block:: bash

   cd IronyAdapter
   pip install . --upgrade

Using your package
==================

If you are creating a module that ChatterBot imports from a dotted module path then you
can set the following in your chat bot.

.. code-block:: python

   chatbot = ChatBot(
       "My ChatBot",
       logic_adapters=[
           "irony_adapter.logic.IronyAdapter"
       ]
   )

Testing your code
=================

.. code-block:: python

   from unittest import TestCase


   class IronyAdapterTestCase(TestCase):
       """
       Test that the irony adapter allows
       the chat bot to understand irony.
       """

       def test_irony(self):
          # TODO: Implement test logic
          self.assertTrue(response.irony)