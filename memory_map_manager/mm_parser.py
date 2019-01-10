#!/usr/bin/env python3
# Copyright (c) 2018 Kevin Weiss, for HAW Hamburg  <kevin.weiss@haw-hamburg.de>
#
# This file is subject to the terms and conditions of the MIT License. See the
# file LICENSE in the top level directory for more details.
# SPDX-License-Identifier:    MIT
"""Parses and manages memory maps from typedefs"""
from copy import deepcopy
from pprint import pformat
from logging import debug, info
from .gen_helpers import PRIM_TYPES


def _copy_elements(typename, config):
    for typedef in config['typedefs']:
        if typename == typedef["type_name"]:
            return {'elements': deepcopy(typedef["elements"])}
    for bitfield in config['bitfields']:
        if typename == bitfield["type_name"]:
            return {'elements': deepcopy(bitfield["elements"])}
    raise ValueError("Cannot find {}".format(typename))


def _copy_typedef_elements(element, config):
    if "array_size" in element:
        array_size = element["array_size"]
        element['array'] = [_copy_elements(element["type"],
                                           config) for i in range(array_size)]
    else:
        element.update(_copy_elements(element["type"], config))


def _expand_typedefs(config):
    for typedef in config["typedefs"]:
        for element in typedef["elements"]:
            if element["type"] not in PRIM_TYPES:
                _copy_typedef_elements(element, config)


def _update_offsets(elements, offset=0):
    for element in elements:
        element["offset"] = offset
        if "elements" in element:
            offset = _update_offsets(element["elements"], offset)
            if "bits" in element["elements"][0]:
                offset += element["type_size"]
        elif "array" in element:
            for array_val in element["array"]:
                offset = _update_offsets(array_val["elements"], offset)
        elif "array_size" in element:
            offset += element["type_size"]*element["array_size"]
        elif "type_size" in element:
            offset += element["type_size"]
    return offset


def _update_access(elements, access):
    for element in elements:
        if 'access' in element:
            overwrite_access = element['access']
        else:
            overwrite_access = access
        if "elements" in element:
            _update_access(element["elements"], access)
            if "bits" in element["elements"][0]:
                element["access"] = overwrite_access
        elif "array" in element:
            for array_val in element["array"]:
                _update_access(array_val["elements"], access)
        element["access"] = overwrite_access


def _expand_mem_maps(config):
    _expand_typedefs(config)
    expanded_mem_maps = []
    for typedef in config['typedefs']:
        if "generate_mem_map" in typedef:
            if typedef["generate_mem_map"] is True:
                if 'access' not in typedef:
                    typedef['access'] = 1
                _update_access(typedef['elements'], typedef['access'])
                _update_offsets(typedef['elements'])
                expanded_mem_maps.append(typedef)
    return expanded_mem_maps


def _parse_elements_to_records(elements, mem_map=None, name=None):
    if mem_map is None:
        mem_map = []
    if name is None:
        name = []
    for element in elements:
        if "elements" in element:
            if "bits" in element["elements"][0]:
                mem_map.append(deepcopy(element))
                mem_map[-1].pop("elements")
                name.append(element["name"])
                mem_map[-1]["name"] = deepcopy(name)
                for bitfield in element["elements"]:
                    mem_map.append(deepcopy(bitfield))
                    mem_map[-1]["type_size"] = element["type_size"]
                    name.append(bitfield["name"])
                    mem_map[-1]["name"] = deepcopy(name)
                    name.pop()
                name.pop()
            else:
                name.append(element["name"])
                _parse_elements_to_records(element["elements"], mem_map, name)
                name.pop()
        elif "array" in element:
            name.append(element["name"])
            for i, array_val in enumerate(element["array"]):
                name.append("%d" % i)
                _parse_elements_to_records(array_val["elements"],
                                           mem_map, name)
                name.pop()
            name.pop()
        else:
            mem_map.append(deepcopy(element))
            name.append(element["name"])
            mem_map[-1]["name"] = deepcopy(name)
            name.pop()
    return mem_map


def _match_k_in_list(list1, list2, match_key='name'):
    """Matches or aligns the values of a given key in two lists of dicts"""
    matching_list = []
    for val1 in list1:
        for val2 in list2:
            if val1[match_key] == val2[match_key]:
                matching_list.append([val1, val2])
    return matching_list


def _import_mem_map_values(config, previous_mem_maps):
    """Imports type_name values from saved memory maps"""
    generated_fields = ['bit_offset', 'bits', 'name', 'offset', 'type_size',
                        'total_size', 'type', 'array_size']
    for matched_mem_map in _match_k_in_list(config['mem_maps'],
                                            previous_mem_maps):
        for matched_record in _match_k_in_list(matched_mem_map[0]['records'],
                                               matched_mem_map[1]['records']):
            for field_name in matched_record[1].keys():
                if field_name not in generated_fields:
                    debug("Matched %r[%r]",
                          matched_record[1]['name'],
                          field_name)
                    val = matched_record[1][field_name]
                    if field_name not in matched_record[0]:
                        matched_record[0][field_name] = val
                    elif matched_record[0][field_name] != val:
                        debug("Replacing %r: %r with %r",
                              field_name, matched_record[0][field_name], val)
                        matched_record[0][field_name] = val


def parse_typedefs_to_mem_maps(config, import_previous_values):
    """Parses a selected (or the last) typedef to a memory map"""
    info("Importing memory maps")
    if import_previous_values:
        previous_mem_maps = deepcopy(config['mem_maps'])
    config['mem_maps'] = []
    for exp_mm in _expand_mem_maps(config):
        mem_map = {'name': exp_mm['type_name']}
        mem_map['records'] = _parse_elements_to_records(exp_mm['elements'])
        config['mem_maps'].append(mem_map)
    if import_previous_values:
        _import_mem_map_values(config, previous_mem_maps)
    debug("Memory maps are:\n%s", pformat(config['mem_maps']))
