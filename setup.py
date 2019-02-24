#!/usr/bin/env python
"""
ChatterBot setup file.
"""
import sys
import platform
from setuptools import setup


if sys.version_info[0] < 3:
    raise Exception(
        'You are tying to install ChatterBot on Python version {}.\n'
        'Please install ChatterBot in Python 3 instead.'.format(
            platform.python_version()
        )
    )

# Dynamically retrieve the version information from the chatterbot module
CHATTERBOT = __import__('chatterbot')
VERSION = CHATTERBOT.__version__
AUTHOR = CHATTERBOT.__author__
AUTHOR_EMAIL = CHATTERBOT.__email__
URL = CHATTERBOT.__url__
DESCRIPTION = CHATTERBOT.__doc__

with open('README.md') as f:
    LONG_DESCRIPTION = f.read()

REQUIREMENTS = []
DEPENDENCIES = []

with open('requirements.txt') as requirements:
    for requirement in requirements.readlines():
        if requirement.startswith('git+git://'):
            DEPENDENCIES.append(requirement)
        else:
            REQUIREMENTS.append(requirement)


setup(
    name='ChatterBot',
    version=VERSION,
    url=URL,
    download_url='{}/tarball/{}'.format(URL, VERSION),
    project_urls={
        'Documentation': 'https://chatterbot.readthedocs.io',
    },
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    packages=[
        'chatterbot',
        'chatterbot.storage',
        'chatterbot.logic',
        'chatterbot.ext',
        'chatterbot.ext.sqlalchemy_app',
        'chatterbot.ext.django_chatterbot',
        'chatterbot.ext.django_chatterbot.migrations',
    ],
    package_dir={'chatterbot': 'chatterbot'},
    include_package_data=True,
    install_requires=REQUIREMENTS,
    dependency_links=DEPENDENCIES,
    python_requires='>=3.4, <4',
    license='BSD',
    zip_safe=True,
    platforms=['any'],
    keywords=['ChatterBot', 'chatbot', 'chat', 'bot'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Communications :: Chat',
        'Topic :: Internet',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3 :: Only',
    ],
    test_suite='tests'
)
