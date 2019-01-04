#!/usr/bin/env python3
# Copyright (c) 2018 Kevin Weiss, for HAW Hamburg  <kevin.weiss@haw-hamburg.de>
#
# This file is subject to the terms and conditions of the MIT License. See the
# file LICENSE in the top level directory for more details.
# SPDX-License-Identifier:    MIT
"""
    Setup file for memory_map_manager.
"""
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()


setup(
    name="memory_map_manager",
    version="0.0.2",
    author="Kevin Weiss",
    author_email="kevin.weiss@haw-hamburg.de",
    license="MIT",
    description="A generator that unifies interfaces for memory maps",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://github.com/riot-appstore/memory_map_manager",
    packages=find_packages(),
    platforms='any',
    python_requires='>=3.5.*',
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers"
    ],
    setup_requires=["pytest-runner"],
    tests_require=["pytest", "pytest-regtest", "pprint"],
    install_requires=["jsonschema"],
    entry_points={
        'console_scripts': ['generate_map=memory_map_manager.code_gen:main'],
    }
)
