#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Note: To use the 'upload' functionality of this file, you must:
#   $ pip install twine

import io
import os

from setuptools import setup

# Package meta-data.
NAME = 'pybrowser'
DESCRIPTION = 'Selenium based, user friendly Browser Automation API'
URL = 'https://github.com/abranjith/pybrowser'
EMAIL = 'abranjith@gmail.com'
AUTHOR = 'Ranjith'
VERSION = '0.2.0'

# What packages are required for this module to be executed?
REQUIRED = [
    'requests', 'selenium==3.141.0', 'pyquery==1.4.0', 'pyppeteer==0.0.25'
]

#here = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long-description.
# Note: this will only work if 'README.rst' is present in your MANIFEST.in file!
#with io.open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
#   long_description = '\n' + f.read()

# Where the magic happens:
setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=DESCRIPTION,
    author=AUTHOR,
    author_email=EMAIL,
    url=URL,
    python_requires='>=3.7.0',
    # If your package is a single module, use this instead of 'packages':
    #py_modules=['pybrowser'],
    packages=['pybrowser', 'pybrowser.elements', 'pybrowser.external'],
    install_requires=REQUIRED,
    include_package_data=True,
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ]
)