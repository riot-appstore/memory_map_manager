#!/usr/bin/env python3
# Copyright (c) 2018 Kevin Weiss, for HAW Hamburg  <kevin.weiss@haw-hamburg.de>
#
# This file is subject to the terms and conditions of the MIT License. See the
# file LICENSE in the top level directory for more details.
# SPDX-License-Identifier:    MIT
"""Setup file for memory_map_manager."""
import re
from setuptools import setup, find_packages

PACKAGE = 'memory_map_manager'
LICENSE = 'MIT'
URL = 'https://github.com/riot-appstore/memory_map_manager'


with open("README.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()


def get_property(prop, project):
    """Get the version from __init__."""
    result = re.search(r'{}\s*=\s*[\'"]([^\'"]*)[\'"]'.format(prop),
                       open(project + '/__init__.py').read())
    return result.group(1)


setup(
    name=PACKAGE,
    version=get_property('__version__', PACKAGE),
    author="Kevin Weiss",
    author_email="kevin.weiss@haw-hamburg.de",
    license=LICENSE,
    description="A generator that unifies interfaces for memory maps",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url=URL,
    packages=find_packages(),
    platforms='any',
    python_requires='>=3.6',
    include_package_data=True,
    classifiers=[
                 'Programming Language :: Python :: 3',
                 'Programming Language :: Python :: 3.5',
                 'Programming Language :: Python :: 3.6',
                 'Programming Language :: Python :: 3.7',
                 'Programming Language :: Python :: 3.8',
                 'Programming Language :: Python :: 3.9',
                 'License :: OSI Approved :: MIT License',
                 'Operating System :: OS Independent',
                 'Development Status :: 3 - Alpha',
                 'Intended Audience :: Developers',
                 'Environment :: Console',
                 'Topic :: Utilities',

    ],
    setup_requires=["pytest-runner"],
    tests_require=["pytest", "pytest-regtest", "pytest-cov"],
    install_requires=["jsonschema"],
    entry_points={
        'console_scripts': ['generate_map=memory_map_manager.code_gen:main'],
    }
)
