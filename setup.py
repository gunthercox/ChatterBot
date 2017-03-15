#!/usr/bin/env python
"""
ChatterBot setup file.
"""
from setuptools import setup


# Dynamically retrieve the version information from the chatterbot module
CHATTERBOT = __import__('chatterbot')
VERSION = CHATTERBOT.__version__
AUTHOR = CHATTERBOT.__author__
AUTHOR_EMAIL = CHATTERBOT.__email__
URL = CHATTERBOT.__url__
DESCRIPTION = CHATTERBOT.__doc__

with open('requirements.txt') as requirements:
    REQUIREMENTS = requirements.readlines()

setup(
    name='ChatterBot',
    version=VERSION,
    url=URL,
    download_url='{}/tarball/{}'.format(URL, VERSION),
    setup_requires=['setuptools-markdown'],
    long_description_markdown_filename='readme.md',
    description=DESCRIPTION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    packages=[
        'chatterbot',
        'chatterbot.input',
        'chatterbot.output',
        'chatterbot.storage',
        'chatterbot.logic',
        'chatterbot.corpus',
        'chatterbot.conversation',
        'chatterbot.ext',
        'chatterbot.ext.django_chatterbot',
        'chatterbot.ext.django_chatterbot.migrations',
        'chatterbot.ext.django_chatterbot.management',
        'chatterbot.ext.django_chatterbot.management.commands'
    ],
    package_dir={'chatterbot': 'chatterbot'},
    include_package_data=True,
    install_requires=REQUIREMENTS,
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
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=['mock']
)
