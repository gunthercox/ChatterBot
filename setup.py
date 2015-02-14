#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

try:
    from pypandoc import convert
    readme = lambda f: convert(f, "rst")
except ImportError:
    print("Module pypandoc not found, could not convert Markdown to RST")
    readme = lambda f: open(f, "r").read()

req = open("requirements.txt")
requirements = req.readlines()

setup(
    name="ChatterBot",
    version="0.1.1",
    url="https://github.com/gunthercox/ChatterBot",
    description="An open-source chat bot program written in Python.",
    long_description=readme("readme.md"),
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
        "Development Status :: 1",
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
