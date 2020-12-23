#!/usr/bin/env python3
# Copyright (c) 2018 Kevin Weiss, for HAW Hamburg  <kevin.weiss@haw-hamburg.de>
#
# This file is subject to the terms and conditions of the MIT License. See the
# file LICENSE in the top level directory for more details.
# SPDX-License-Identifier:    MIT
"""Fills in any missing/calculatable information of typedefs"""
from copy import deepcopy
from logging import debug, info
from pprint import pformat
from .gen_helpers import PRIM_TYPES


def _assert_val_is_unique(dict_list, key_name):
    used_names = []
    for target_dict in dict_list:
        if target_dict[key_name] in used_names:
            raise ValueError("{} is a duplicate name".
                             format(target_dict[key_name]))
        used_names.append(target_dict[key_name])


def _update_bitfields(config):
    info("Updating bitfields from typedef")

    for bitfield in config['bitfields']:
        bit_offset = 0
        for element in bitfield['elements']:
            element['bit_offset'] = bit_offset
            bit_offset += element['bits']
        if 'type' not in bitfield:
            bitfield['type'] = 'uint8_t'
        bitfield['type_size'] = PRIM_TYPES[bitfield['type']]
        if bit_offset > bitfield['type_size']*8:
            raise ValueError("Bits do not fit into type, {} -> {}bits > {}".
                             format(bitfield['type_name'],
                                    bit_offset,
                                    bitfield['type']))
        if bit_offset != bitfield['type_size']*8:
            _fill_bitfield_res_element(bitfield, bit_offset)
    _assert_val_is_unique(config['bitfields'], 'type_name')
    debug("bitfields are now:\n%s", pformat(config['bitfields']))


def _fill_bitfield_res_element(bitfield, bit_offset):
    res = {'name': 'res',
           'bits': (bitfield['type_size'] * 8) - bit_offset,
           'bit_offset': bit_offset,
           'description': 'Reserved bits'}
    bitfield['elements'].append(res)
    debug("Adding bitfield reserved element to %r of size %r",
          bitfield['type_name'], res['bits'])


def _fill_res_element(typedef, total_byte):
    res = {'name': 'res',
           'type': 'uint8_t',
           'array_size': typedef['type_size'] - total_byte,
           'type_size': 1,
           'total_size': typedef['type_size'] - total_byte,
           'description': 'Reserved bytes',
           'access': 0x00}
    typedef['elements'].append(res)
    debug("Adding reserved element to %r of size %r",
          typedef['type_name'], res['total_size'])


def _update_typedefs_sizes(config, type_sizes):
    info("Updating typedef sizes")
    for typedef in config['typedefs']:
        total_byte = 0
        for element in typedef['elements']:
            element["type_size"] = type_sizes[element["type"]]

            if 'array_size' in element:
                element["total_size"] = element["type_size"]\
                                        * element["array_size"]
                total_byte += element["total_size"]
            else:
                total_byte += element["type_size"]

        if 'type_size' in typedef:
            if typedef['type_size'] < total_byte:
                raise ValueError("{} to large".format(typedef["name"]))

            if typedef['type_size'] is not total_byte:
                _fill_res_element(typedef, total_byte)
        else:
            typedef['type_size'] = total_byte
        type_sizes[typedef["type_name"]] = typedef["type_size"]


def update_typedefs(config):
    """Fill in any missing/calculable information of typedefs."""
    info("Updating typedefs from config")
    type_sizes = deepcopy(PRIM_TYPES)
    _update_bitfields(config)
    for bitfield in config['bitfields']:
        type_sizes[bitfield['type_name']] = bitfield['type_size']

    _update_typedefs_sizes(config, type_sizes)
    for typedef in config['typedefs']:
        type_sizes[typedef["type_name"]] = typedef["type_size"]
    _assert_val_is_unique(config['typedefs'], 'type_name')
