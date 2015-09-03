#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

req = open("requirements.txt")
requirements = req.readlines()

# Dynamically calculate the version based on chatterbot version
version = __import__('chatterbot').__version__

setup(
    name="ChatterBot",
    version=version,
    url="https://github.com/gunthercox/ChatterBot",
    setup_requires=['setuptools-markdown'],
    long_description_markdown_filename='readme.md',
    description="An open-source chat bot program written in Python.",
    author="Gunther Cox",
    author_email="gunthercx@gmail.com",
    packages=find_packages(),
    package_dir={"chatterbot": "chatterbot"},
    include_package_data=True,
    install_requires=requirements,
    license="BSD",
    zip_safe=False,
    platforms=["any"],
    keywords=["ChatterBot", "chatbot", "chat", "bot"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Environment :: Console",
        "Environment :: Web Environment",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
    ],
    test_suite="tests",
    tests_require=[]
)
