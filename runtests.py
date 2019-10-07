#!/usr/bin/env python

"""
This is the test runner for the ChatterBot's Django tests.
"""

import os
import sys
import numpy as np

import django
from django.conf import settings
from django.test.utils import get_runner

if __name__ == '__main__':
    os.environ['DJANGO_SETTINGS_MODULE'] = 'tests_django.test_settings'
    django.setup()
    TestRunner = get_runner(settings)
    test_runner = TestRunner(
        verbosity=2

    )
    
    failures = test_runner.run_tests(['tests_django'])
    if bool(failures)==1:
        sys.exit()
        
