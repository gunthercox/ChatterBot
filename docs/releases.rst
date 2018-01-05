====================
Releasing ChatterBot
====================

ChatterBot follows the following rules when it comes to new versions and updates.

Versioning
==========

ChatterBot follows semantic versioning as a set of guidelines for release versions.

- **Major** releases (2.0.0, 3.0.0, etc.) are used for large, almost
  entirely backwards incompatible changes.

- **Minor** releases (2.1.0, 2.2.0, 3.1.0, 3.2.0, etc.) are used for
  releases that contain small, backwards incompatible changes. Known
  backwards incompatibilities will be described in the release notes.

- **Patch** releases (e.g., 2.1.1, 2.1.2, 3.0.1, 3.0.10, etc.) are used
  for releases that contain bug fixes, features and dependency changes.


Release Process
===============

The following procedure is used to finalize a new version of ChatterBot.

1. We make sure that all CI tests on the master branch are passing.

2. We tag the release on GitHub.

3. A new package is generated from the latest version of the master branch.

.. code-block:: bash

   python setup.py sdist bdist_wheel

4. The Python package files are uploaded to PyPi.

.. code-block:: bash

   twine upload dist/*
