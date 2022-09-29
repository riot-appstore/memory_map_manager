#!/usr/bin/env python3
# Copyright (c) 2018 Kevin Weiss, for HAW Hamburg  <kevin.weiss@haw-hamburg.de>
#
# This file is subject to the terms and conditions of the MIT License. See the
# file LICENSE in the top level directory for more details.
# SPDX-License-Identifier:    MIT
"""Setup file for memory_map_manager."""
import os
from setuptools import setup


def get_version():
    """Extract package version without importing file.

    Importing cause issues with coverage,
        (modules can be removed from sys.modules to prevent this)
    Importing __init__.py triggers importing rest and then requests too
    Inspired from pep8 setup.py
    """
    with open(os.path.join('memory_map_manager', "_version.py")) as init_fd:
        for line in init_fd:
            if line.startswith("__version__"):
                return eval(line.split("=")[-1])  # pylint:disable=eval-used
    return None


setup(
    version=get_version(),
    setup_requires=["pytest-runner"],
)
