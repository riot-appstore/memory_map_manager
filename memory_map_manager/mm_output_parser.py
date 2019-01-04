#!/usr/bin/env python3
# Copyright (c) 2018 Kevin Weiss, for HAW Hamburg  <kevin.weiss@haw-hamburg.de>
#
# This file is subject to the terms and conditions of the MIT License. See the
# file LICENSE in the top level directory for more details.
# SPDX-License-Identifier:    MIT
"""This module generates output files based on memory maps."""
from copy import deepcopy
from logging import debug, info


def _insert_at_front(field_names, name):
    if name in field_names:
        field_names.insert(0, field_names.pop(field_names.index(name)))


def _find_unique_keys(records):
    info("Finding unique keys")
    field_names = []
    for record in records:
        for field_name in record.keys():
            if field_name not in field_names:
                debug("Found %r", field_name)
                field_names.append(field_name)
    field_names = sorted(field_names)
    # Ordered but starts with name, offset, total_size, description
    _insert_at_front(field_names, 'description')
    _insert_at_front(field_names, 'type')
    _insert_at_front(field_names, 'type_size')
    _insert_at_front(field_names, 'total_size')
    _insert_at_front(field_names, 'offset')
    _insert_at_front(field_names, 'name')

    return field_names


def _get_name(names):
    full_name = ''
    for name in names:
        if name.isdigit():
            full_name = '{}[{}].'.format(full_name[:-1], name)
        else:
            full_name += '{}.'.format(name)
    return full_name[:-1]


def parse_mem_map_to_csv(mem_map):
    """Parses a memory map to a csv table string."""
    info("Parsing memory map to csv string")
    local_mem_map = deepcopy(mem_map)
    fields = _find_unique_keys(local_mem_map['records'])
    csv_str = ','.join(fields)
    for record in local_mem_map['records']:
        csv_str += '\n'
        name = _get_name(record['name'])
        for field in fields:
            if field not in record:
                record[field] = ''
            if record[field] is None:
                record[field] = ''
            if field == 'name':
                csv_str += name
            else:
                csv_str += str(record[field]).replace(',', '","')
            csv_str += ','
        csv_str = csv_str[:-1]
    return csv_str


def parse_mem_map_to_access_c(mem_maps):
    """Parses access registers based on memory map to a .c string."""
    a_str = "#include \"app_access.h\"\n"
    for mem_map in deepcopy(mem_maps):
        a_str += "\nconst uint8_t %s_ACCESS[] = { \n" % mem_map['name'].upper()
        size = 0
        map_size = 0
        for record in mem_map['records']:
            debug(record)
            if 'bit_offset' not in record:
                size = record['type_size']
                if 'total_size' in record:
                    size = record['total_size']
                for access_byte in range(size):
                    if access_byte != 0:
                        a_str += ", "
                    a_str += "0x%02X" % record["access"]
                    size += 1
                    map_size += 1
                if record != mem_map['records'][-1]:
                    a_str += ","
                a_str += " /* {} */\n".format('_'.join(record["name"]))
        a_str = a_str.rstrip(',')
        a_str += "/* total size %d */\n};" % map_size
    return a_str
