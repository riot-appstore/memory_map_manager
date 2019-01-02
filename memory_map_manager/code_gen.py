#!/usr/bin/env python3
# Copyright (c) 2018 Kevin Weiss, for HAW Hamburg  <kevin.weiss@haw-hamburg.de>
#
# This file is subject to the terms and conditions of the MIT License. See the
# file LICENSE in the top level directory for more details.
# SPDX-License-Identifier:    MIT
"""This module handles parsing of typedefs and creating outputs"""
import os
import argparse
import logging
from copy import deepcopy
from pprint import pprint
from .td_parser import update_typedefs
from .td_output_parser import parse_typedefs_to_h
from .mm_parser import parse_typedefs_to_mem_maps
from .mm_output_parser import parse_mem_map_to_csv, parse_mem_map_to_access_c
from .config_import_export import import_config, export_config

LOG_HANDLER = logging.StreamHandler()
LOG_HANDLER.setFormatter(logging.Formatter(logging.BASIC_FORMAT))

LOG_LEVELS = ('debug', 'info', 'warning', 'error', 'fatal', 'critical')


PARSER = argparse.ArgumentParser()

PARSER.add_argument("--config_path", "-cfgp",
                    help='The path to the config file or directory',
                    default='')

PARSER.add_argument("--output_config", "-ocfg",
                    help='The path and name of the output config file')

PARSER.add_argument("--output_dir", "-odir",
                    help='The path for all generated output',
                    default='')

PARSER.add_argument("--reset_config", "-rcfg",
                    help='Dont copy previous non-generated mem map values',
                    action='store_true',
                    default=False)

PARSER.add_argument("--only_update_config", "-ouc",
                    help='Only updates config file without generating files',
                    action='store_true',
                    default=False)

PARSER.add_argument("--print_config", "-pcfg",
                    help='Prints the config to stdout',
                    action='store_true',
                    default=False)

PARSER.add_argument('--loglevel', choices=LOG_LEVELS, default='info',
                    help='Python logger log level, defaults to "info"')


def main():
    """Parses typedefs and creates outputs"""

    args = PARSER.parse_args()
    if args.loglevel:
        loglevel = logging.getLevelName(args.loglevel.upper())
        logging.basicConfig(level=loglevel)
    logging.info("Starting memory_map_manager")

    if args.config_path.startswith('/'):
        config_path = args.config_path
    else:
        config_path = os.path.join(os.getcwd(), args.config_path)
    config = import_config(config_path)
    imported_config = deepcopy(config)
    update_typedefs(config)
    parse_typedefs_to_mem_maps(config, (args.reset_config is False))

    imported_config['mem_maps'] = deepcopy(config['mem_maps'])
    if args.output_config is not None:
        export_config(imported_config, args.output_config)
    else:
        export_config(imported_config, config_path)

    if args.print_config:
        pprint(imported_config)

    if args.only_update_config:
        return

    if args.output_dir.startswith('/'):
        output_dir = args.config_path
    else:
        output_dir = os.path.join(os.getcwd(), args.output_dir)

    filename = config['metadata']['app_name']
    with open(os.path.join(output_dir, filename + '_typedef.h'), "w") as out_f:
        out_f.write(parse_typedefs_to_h(config))

    for mem_map in config['mem_maps']:
        with open(os.path.join(output_dir,
                               mem_map['name'] + '.csv'), "w") as out_f:
            out_f.write(parse_mem_map_to_csv(mem_map))

    with open(os.path.join(output_dir, 'access.c'), "w") as out_f:
        out_f.write(parse_mem_map_to_access_c(config['mem_maps']))


if __name__ == "__main__":
    main()
