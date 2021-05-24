#!/usr/bin/env python
from __future__ import print_function
from setuptools import setup, find_packages
import sys

setup(
    name="threp",
    version="2.0.0b",
    author="wasupandceacar",
    author_email="wasupandceacar@gmail.com",
    description="decode Touhou Shooting Game's replay files and get the infomation in it",
    license="MIT",
    long_description=open('README.rst', encoding='UTF-8').read(),
    url="https://github.com/wasupandceacar/threp",
    packages=['threp'],
    install_requires=[],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Games/Entertainment",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    keywords='touhou replay python',
)
