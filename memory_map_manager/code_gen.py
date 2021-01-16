#!/usr/bin/env python3
# Copyright (c) 2018 Kevin Weiss, for HAW Hamburg  <kevin.weiss@haw-hamburg.de>
#
# This file is subject to the terms and conditions of the MIT License. See the
# file LICENSE in the top level directory for more details.
# SPDX-License-Identifier:    MIT
"""This module handles parsing of typedefs and creating outputs."""
import os
import argparse
import logging
from copy import deepcopy
from pprint import pprint
from .td_parser import update_typedefs
from .td_output_parser import parse_typedefs_to_h
from .mm_parser import parse_typedefs_to_mem_maps
from .mm_output_parser import parse_mem_map_to_csv, parse_mem_map_to_access_c
from .mm_output_parser import parse_mem_map_to_defaults_h
from .mm_output_parser import parse_mem_map_to_map_v_c
from .mm_output_parser import parse_mem_map_to_map_v_h
from .mm_output_parser import parse_mem_map_to_defaults_c
from .config_import_export import import_config, export_config

LOG_HANDLER = logging.StreamHandler()
LOG_HANDLER.setFormatter(logging.Formatter(logging.BASIC_FORMAT))

LOG_LEVELS = ('debug', 'info', 'warning', 'error', 'fatal', 'critical')


PARSER = argparse.ArgumentParser()

PARSER.add_argument("--config-path", "-P",
                    help='The path to the config file or directory',
                    default='')

PARSER.add_argument("--output-config", "-c",
                    help='The path and name of the output config file')

PARSER.add_argument("--output-dir", "-D",
                    help='The path for all generated output',
                    default='')

PARSER.add_argument("--output-csv", "-o",
                    help='The path for the csv memory map',
                    default='')

PARSER.add_argument("--reset-config", "-r",
                    help='Do not copy previous non-generated mem map values',
                    action='store_true',
                    default=False)

PARSER.add_argument("--only-update-config", "-u",
                    help='Only updates config file without generating files',
                    action='store_true',
                    default=False)

PARSER.add_argument("--print-date", "-d",
                    help='prints the date in all headers',
                    action='store_true',
                    default=False)

PARSER.add_argument("--print-config", "-p",
                    help='Prints the config to stdout',
                    action='store_true',
                    default=False)

PARSER.add_argument('--loglevel', choices=LOG_LEVELS, default='info',
                    help='Python logger log level, defaults to "info"')


def main():  # pylint: disable=too-many-branches
    """Parse typedefs and create outputs."""
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
        output_dir = args.output_dir
    else:
        output_dir = os.path.join(os.getcwd(), args.output_dir)

    if args.output_csv:
        if args.output_csv.startswith('/'):
            output_csv = args.output_csv
        else:
            output_csv = os.path.join(os.getcwd(), args.output_csv)
    else:
        output_csv = output_dir

    filename = config['metadata']['app_name']
    if_version = config['metadata']['version'].replace('.', '_')
    with open(os.path.join(output_dir, filename + '_typedef.h'), "w") as opf:
        opf.write(parse_typedefs_to_h(config, args.print_date))

    for mem_map in config['mem_maps']:
        csv_fn = '{}_{}_{}.csv'.format(filename, mem_map['name'], if_version)
        with open(os.path.join(output_csv, csv_fn), "w") as opf:
            opf.write(parse_mem_map_to_csv(mem_map))

    with open(os.path.join(output_dir, filename + '_access.c'), "w") as opf:
        opf.write(parse_mem_map_to_access_c(config, args.print_date))

    with open(os.path.join(output_dir, filename + '_map.c'), "w") as opf:
        opf.write(parse_mem_map_to_map_v_c(config, args.print_date))
    with open(os.path.join(output_dir, filename + '_map.h'), "w") as opf:
        opf.write(parse_mem_map_to_map_v_h(config, args.print_date))

    with open(os.path.join(output_dir, filename + '_defaults.h'), "w") as opf:
        opf.write(parse_mem_map_to_defaults_h(config, args.print_date))

    with open(os.path.join(output_dir, filename + '_defaults.c'), "w") as opf:
        opf.write(parse_mem_map_to_defaults_c(config, args.print_date))


if __name__ == "__main__":
    main()
