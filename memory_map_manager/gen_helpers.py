#!/usr/bin/env python3
# Copyright (c) 2018 Kevin Weiss, for HAW Hamburg  <kevin.weiss@haw-hamburg.de>
#
# This file is subject to the terms and conditions of the MIT License. See the
# file LICENSE in the top level directory for more details.
# SPDX-License-Identifier:    MIT
"""This module contains helpers for the code generator"""

PRIM_TYPES = {'uint8_t': 1, 'int8_t': 1, 'uint16_t': 2, 'int16_t': 2,
              'uint32_t': 4, 'int32_t': 4, 'uint64_t': 8, 'int64_t': 8,
              'char': 1, 'float': 4, 'double': 8}
