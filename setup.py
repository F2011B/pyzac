#!/bin/env python

"""
Setup script for rinohtype
"""

import os
import sys

from setuptools import setup, find_packages


BASE_PATH = os.path.dirname(os.path.abspath(__file__))


if sys.version_info < (3, 3):
    print("pyzac requires Python 3.3 or higher")
    sys.exit(1)


def long_description():
    with open(os.path.join(BASE_PATH, "README.rst")) as readme:
        result = readme.read()
    result += "\n\n"
    with open(os.path.join(BASE_PATH, "CHANGES.rst")) as changes:
        result += changes.read()
    return result


setup(
    name="pyzac",
    version="0.1.2",
    packages=find_packages("src"),
    package_dir={"": "src"},
    include_package_data=True,
    python_requires=">= 3.3",
    license="Apache 2.0",
    # install_requires=["setuptools", "pip", "docutils", "purepng>=0.1.1"],
    # extras_require={"bitmap": ["Pillow"]},
    # setup_requires=["pytest-runner"],
    # tests_require=["pytest>=2.0.0", "pytest-assume", "requests", "PyPDF2"],
    author="Dark Ligt alias FB2011B",
    description="The Python Actor Model using zeroMQ",
    long_description=open("README.rst").read(),
    url="https://github.com/F2011B/pyzac",
    keywords="actor zeromq pzmq",
    classifiers=[
        "Environment :: Console",
        "Environment :: Other Environment",
        "Environment :: Web Environment",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
