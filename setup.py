#!/usr/bin/env python

from setuptools import setup


# Dynamically retrieve the version information from the chatterbot module
version = __import__('chatterbot').__version__
author = __import__('chatterbot').__author__
author_email = __import__('chatterbot').__email__

req = open('requirements.txt')
requirements = req.readlines()
req.close()

setup(
    name='ChatterBot',
    version=version,
    url='https://github.com/gunthercox/ChatterBot',
    setup_requires=['setuptools-markdown'],
    long_description_markdown_filename='readme.md',
    description='An open-source chat bot program written in Python.',
    author=author,
    author_email=author_email,
    packages=[
        'chatterbot',
        'chatterbot.adapters',
        'chatterbot.adapters.input',
        'chatterbot.adapters.output',
        'chatterbot.adapters.storage',
        'chatterbot.adapters.logic',
        'chatterbot.corpus',
        'chatterbot.conversation',
        'chatterbot.training',
        'chatterbot.utils'
    ],
    package_dir={'chatterbot': 'chatterbot'},
    include_package_data=True,
    install_requires=requirements,
    license='BSD',
    zip_safe=False,
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
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=['mock']
)
