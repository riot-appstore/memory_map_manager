#!/usr/bin/env python3
# Copyright (c) 2018 Kevin Weiss, for HAW Hamburg  <kevin.weiss@haw-hamburg.de>
#
# This file is subject to the terms and conditions of the MIT License. See the
# file LICENSE in the top level directory for more details.
# SPDX-License-Identifier:    MIT
"""This module generates output files based on memory maps."""
import re
from copy import deepcopy
from logging import debug, info
from .gen_helpers import get_header, try_key, PRIM_ENUM_LIST, PRIM_TYPES


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
    """Parse a memory map to a csv table string."""
    info("Parsing memory map to csv string")
    local_mem_map = deepcopy(mem_map)
    fields = _find_unique_keys(local_mem_map['records'])
    csv_str = ','.join(fields)
    for record in local_mem_map['records']:
        if 'bits' not in record:
            if record['type'] not in PRIM_TYPES:
                continue
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
    csv_str += '\n'
    return csv_str


def _records_to_string_array(key_name, mem_map, print_val=True):
    arr_str = "const char* const {}_{}[]".format(mem_map['name'].upper(),
                                                 key_name.upper())
    if print_val is False:
        arr_str += "; /** < {} const array */\n".format(key_name)
        return "extern " + arr_str
    arr_str += " = {"
    for record in mem_map['records']:
        name = '\"{}\",\n'.format('.'.join(record[key_name]))
        arr_str += re.sub(r'\.(\d+)', r'[\1]', name)
    arr_str = arr_str.rstrip(',\n')
    arr_str += "}}; /** < {} const array */\n".format(key_name)
    return arr_str


def _records_to_int_array(key_name, mem_map, print_val=True):
    max_val = 0
    for record in mem_map['records']:
        if key_name not in record or record[key_name] is None:
            record[key_name] = 0
        if record[key_name] > max_val:
            max_val = record[key_name]
    if max_val < 0x100:
        arr_str = "const uint8_t {}_{}[]".format(mem_map['name'].upper(),
                                                 key_name.upper())
    elif max_val < 0x10000:
        arr_str = "const uint16_t {}_{}[]".format(mem_map['name'].upper(),
                                                  key_name.upper())
    else:
        arr_str = "const uint32_t {}_{}[]".format(mem_map['name'].upper(),
                                                  key_name.upper())

    if print_val is False:
        arr_str += "; /** < {} const array */\n".format(key_name)
        return "extern " + arr_str
    arr_str += " = {"
    for record in mem_map['records']:
        arr_str += '{},\n'.format(record[key_name])
    arr_str = arr_str.rstrip(',\n')
    arr_str += "}}; /** < {} const array */\n".format(key_name)
    return arr_str


def _records_type_to_array(mem_map, print_val=True):
    arr_str = "const uint8_t {}_TYPE[]".format(mem_map['name'].upper())
    if print_val is False:
        arr_str += "; /** < type const array */\n"
        return "extern " + arr_str
    arr_str += " = {"
    for record in mem_map['records']:
        try:
            arr_str += '{},\n'.format(PRIM_ENUM_LIST.index(record['type']))
        except (ValueError, KeyError):
            backup_type = 'uint8_t'
            if record['type_size'] == 2:
                backup_type = 'uint16_t'
            elif record['type_size'] == 4:
                backup_type = 'uint32_t'
            elif record['type_size'] == 8:
                backup_type = 'uint64_t'
            arr_str += '{},\n'.format(PRIM_ENUM_LIST.index(backup_type))
    arr_str = arr_str.rstrip(',\n')
    arr_str += "}; /** < type_name const array */\n"

    return arr_str


def _parse_defaults(mem_map):
    defaults = []
    for record in mem_map['records']:
        if 'default' in record:
            default = {}
            default['def_name'] = "DEFAULT_{}".format(".".join(record["name"]))
            default['def_name'] = default['def_name'].upper()
            default['def_name'] = default['def_name'].replace('.', '_')
            default['value'] = int(record['default'])
            default['struct_name'] = _get_name(record['name'])
            default['desc'] = try_key(record, 'description')
            defaults.append(default)
    return defaults


def parse_mem_map_to_defaults_c(config, date_in_header=False):
    """Parses memory map defaults if any to defines in header file"""
    metadata = config['metadata']
    d_str = get_header(metadata, 'defaults.c', 'MMM', date_in_header)
    d_str += "/* Includes ---------------------------------------------------"
    d_str += "---------------*/\n"
    d_str += "#include <stdint.h>\n\n"
    d_str += "#include \"{}_typedef.h\"\n".format(metadata['app_name'])
    d_str += "#include \"{}_defaults.h\"\n\n".format(metadata['app_name'])
    d_str += "/* Functions ---------------------------------------------------"
    d_str += "--------------*/\n"
    for mem_map in deepcopy(config['mem_maps']):
        name = mem_map['name']
        d_str += "/** @brief Assign defaults for {} */\n".format(name)
        d_str += "void init_defaults_{0}({0} *init)".format(name)
        d_str += " {\n"
        defaults = _parse_defaults(mem_map)
        for default in defaults:
            var_name = "init->{}".format(default['struct_name'])
            d_str += "\t{} = {};\n".format(var_name, default['def_name'])
        d_str += "}\n\n"
    return d_str


def parse_mem_map_to_defaults_h(config, date_in_header=False):
    """Parses memory map defaults to initiate in a c file"""
    metadata = config['metadata']
    d_str = get_header(metadata, 'defaults.h', 'MMM', date_in_header)
    d_str += "/* Defines -----------------------------------------------------"
    d_str += "--------------*/\n"
    for mem_map in deepcopy(config['mem_maps']):
        defaults = _parse_defaults(mem_map)
        name = mem_map['name']
        for default in defaults:
            d_str += "/** @brief default for "
            d_str += "{}: {} */\n".format(default['struct_name'],
                                          default['desc'])
            d_str += "#define {} {}\n".format(default['def_name'],
                                              default['value'])
        d_str += "\n/** @brief Assign defaults for {} */\n".format(name)
        d_str += "void init_defaults_{0}({0} *init);\n".format(name)
    d_str += "\n#endif /* %s_DEFAULTS_H */\n" % (metadata["app_name"].upper())
    d_str += "/** @} */\n"
    return d_str


def parse_mem_map_to_map_v_c(config, date_in_header=False):
    """Parses memory map to c arrays with values"""
    kw_str = get_header(config['metadata'], 'map.c', 'MMM', date_in_header)
    app_name = config['metadata']["app_name"]
    kw_str += """\
/* Includes ----------------------------------------------------------------*/
#include <stdint.h>

#include \"{}_map.h\"

/* Global variables --------------------------------------------------------*/
""".format(app_name)
    kw_str += "const char* const {}_TYPE_NAME[] = {{".format(app_name.upper())
    for prim_enum_name in PRIM_ENUM_LIST:
        kw_str += '\"{}\",\n'.format(prim_enum_name)
    kw_str = kw_str.rstrip(',\n')
    kw_str += "}; /** < type_name enum */\n\n"

    kw_str += "const uint8_t  {}_TYPE_SIZE[] = {{".format(app_name.upper())
    for prim_enum_name in PRIM_ENUM_LIST:
        kw_str += '{},\n'.format(PRIM_TYPES[prim_enum_name])
    kw_str = kw_str.rstrip(',\n')
    kw_str += "}; /** <  type_size const array */\n\n"

    for mem_map in deepcopy(config['mem_maps']):
        kw_str += '{}\n'.format(_records_to_string_array('name', mem_map))
        kw_str += '{}\n'.format(_records_to_int_array('offset', mem_map))
        kw_str += '{}\n'.format(_records_type_to_array(mem_map))
        kw_str += '{}\n'.format(_records_to_int_array('array_size', mem_map))
        kw_str += '{}\n'.format(_records_to_int_array('bit_offset', mem_map))
        kw_str += '{}\n'.format(_records_to_int_array('bits', mem_map))
    return kw_str


def parse_mem_map_to_map_v_h(config, date_in_header=False):
    """Parse memory map to h arrays with values."""
    kw_str = get_header(config['metadata'], 'map.h', 'MMM', date_in_header)
    vers = config['metadata']['version'].split(".")
    kw_str += """\
/* Defines ----------------------------------------------------------------- */
#define IF_VERSION_MAJOR {0} /**< Major version of interface */
#define IF_VERSION_MINOR {1} /**< Minor version of interface */
#define IF_VERSION_PATCH {2} /**< Patch version of interface */

/* Global variables -------------------------------------------------------- */
extern const char* const {3}_TYPE_NAME[]; /** < type_name enum */
extern const uint8_t  {3}_TYPE_SIZE[]; /** <  type_size const array */

""".format(int(vers[0]), int(vers[1]), int(vers[2]),
           config['metadata']['app_name'].upper())
    for mem_map in deepcopy(config['mem_maps']):
        kw_str += """\
#define {}_NUM_OF_RECORDS {} /**< Number of records in the map */

""".format(mem_map['name'].upper(), len(mem_map['records']))

        kw_str += '{}'.format(_records_to_string_array('name', mem_map,
                                                       False))
        kw_str += '{}'.format(_records_to_int_array('offset', mem_map,
                                                    False))
        kw_str += '{}'.format(_records_type_to_array(mem_map, False))
        kw_str += '{}'.format(_records_to_int_array('array_size', mem_map,
                                                    False))
        kw_str += '{}'.format(_records_to_int_array('bit_offset', mem_map,
                                                    False))
        kw_str += '{}'.format(_records_to_int_array('bits', mem_map,
                                                    False))
    kw_str += "#endif /* "
    kw_str += "%s_MAP_H */\n" % (config['metadata']["app_name"].upper())
    kw_str += "/** @} */\n"
    return kw_str


def parse_mem_map_to_access_c(config, date_in_header=False):
    """Parse access registers based on memory map to a .c string."""
    a_str = get_header(config['metadata'], 'access.c', 'MMM', date_in_header)
    a_str += """\
/* Includes -----------------------------------------------------------------*/
#include <stdio.h>

/* Global variables ---------------------------------------------------------*/
"""
    for mem_map in deepcopy(config['mem_maps']):
        a_str += "const uint8_t %s_ACCESS[] = { \n" % mem_map['name'].upper()
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
        a_str += "};/**< access array total size %d */\n" % map_size
    return a_str
