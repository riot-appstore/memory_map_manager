#!/usr/bin/env python3
# Copyright (c) 2018 Kevin Weiss, for HAW Hamburg  <kevin.weiss@haw-hamburg.de>
#
# This file is subject to the terms and conditions of the MIT License. See the
# file LICENSE in the top level directory for more details.
# SPDX-License-Identifier:    MIT
"""This module contains helpers for the code generator"""
import datetime
from memory_map_manager import __version__

PRIM_TYPES = {'uint8_t': 1, 'int8_t': 1, 'uint16_t': 2, 'int16_t': 2,
              'uint32_t': 4, 'int32_t': 4, 'uint64_t': 8, 'int64_t': 8,
              'char': 1, 'float': 4, 'double': 8}

PRIM_ENUM_LIST = ['uint8_t', 'int8_t', 'uint16_t', 'int16_t',
                  'uint32_t', 'int32_t', 'uint64_t', 'int64_t',
                  'char', 'float', 'double']


def get_header(metadata, filename, group_suffix, date_in_header=False):
    """Parse a generic .c or .h header."""
    intro_str = ""
    intro_str += """\
/**
 *****************************************************************************"
 * @addtogroup {0}_{1}
 * @{{
 * @file      {0}_{2}
 * @author    {3}
 * @version   {4}
""".format(metadata["app_name"], group_suffix, filename, metadata["author"],
           metadata["version"])
    if date_in_header:
        intro_str += "* @date      {}\n".format(datetime.date.today())
    if "description" in metadata:
        intro_str += " * @brief     {}\n".format(metadata["description"])
    if not filename.endswith('.h'):
        intro_str += " * @}\n"
    intro_str += """\
 * @details   Generated from the memory map manager version {}
 *****************************************************************************"
 */
""".format(__version__)

    if filename.endswith('.h'):
        h_str = filename.upper().replace('.', '_')
        app_name = metadata["app_name"].upper()
        intro_str += "#ifndef %s_%s\n" % (app_name, h_str)
        intro_str += "#define %s_%s\n\n" % (app_name, h_str)
    return intro_str


def try_key(dict_to_try, key_for_dict):
    """Either returns key value or empty string."""
    if key_for_dict not in dict_to_try:
        return ''
    return dict_to_try[key_for_dict]
