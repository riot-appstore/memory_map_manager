# coding=utf-8
# Copyright (c) 2022 Kevin Weiss, for HAW Hamburg  <kevin.weiss@haw-hamburg.de>
#
# This file is subject to the terms and conditions of the MIT License. See the
# file LICENSE in the top level directory for more details.
# SPDX-License-Identifier:    MIT
"""Code generation tool for c and python memory map management.

Exposes the public classes for generation.
"""
from ._version import __version__ as MMM_VERSION
from .importer import MMMImporter
from .mmm_config_parser import MMMConfigParser
from .exporter import MMMExporter


__all__ = ['MMMImporter',
           'MMMConfigParser',
           'MMMExporter',
           'MMM_VERSION']
