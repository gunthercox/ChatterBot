"""
Django integration tests for ChatterBot.

This package contains tests that require Django to be installed.
If Django is not available, these tests will be gracefully skipped.
"""

import os
import sys

# Check if Django is available
try:
    import django
    DJANGO_AVAILABLE = True

    # Configure Django settings immediately upon import
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tests.django_integration.test_settings')

    try:
        django.setup()
    except Exception as e:
        print(f"Warning: Django setup failed: {e}", file=sys.stderr)
        DJANGO_AVAILABLE = False

except ImportError:
    DJANGO_AVAILABLE = False


def load_tests(loader, tests, pattern):
    """
    Custom test loader that configures Django before running tests.

    This function is called automatically by unittest's discovery mechanism.
    If Django is not installed, it returns an empty test suite.
    """
    if not DJANGO_AVAILABLE:
        # Return empty test suite if Django is not available
        import unittest
        return unittest.TestSuite()

    # Load all tests from this package
    package_tests = loader.discover(
        start_dir=os.path.dirname(__file__),
        pattern=pattern or 'test*.py',
        top_level_dir=os.path.dirname(os.path.dirname(__file__))
    )

    return package_tests
